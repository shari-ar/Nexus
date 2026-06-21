#!/usr/bin/env python3
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT_DIR = Path(__file__).resolve().parents[2]
AGENTS_DIR = ROOT_DIR / "configs" / "agents"
MODELS_DIR = ROOT_DIR / "configs" / "models"
PROMPTS_DIR = ROOT_DIR / "prompts"
CONTRACTS_DIR = ROOT_DIR / "orchestration" / "shared" / "contracts"
PERMISSIONS_FILE = ROOT_DIR / "configs" / "system" / "permissions.yaml"
WORKFLOWS_DIR = ROOT_DIR / "configs" / "workflows"
REQUIRED_AGENTS = ["supervisor", "planner", "reviewer", "coding", "documentation", "devops"]
REQUIRED_AGENT_FIELDS = [
    "id",
    "display_name",
    "version",
    "role",
    "responsibility",
    "boundary",
    "prompt_template",
    "shared_policy_template",
    "model_profile",
    "permission_policy",
    "allowed_tools",
    "input_contract",
    "output_contract",
    "validation",
]


def fail(message):
    print(f"invalid: {message}", file=sys.stderr)
    return False


def load_yaml(path):
    if yaml is not None:
        with path.open("r", encoding="utf-8") as file_handle:
            return yaml.safe_load(file_handle)
    return load_simple_yaml(path)


def load_simple_yaml(path):
    result = {}
    stack = [(0, result)]
    with path.open("r", encoding="utf-8") as file_handle:
        for raw_line in file_handle:
            if not raw_line.strip() or raw_line.lstrip().startswith("#"):
                continue
            indent = len(raw_line) - len(raw_line.lstrip(" "))
            line = raw_line.strip()
            while stack and indent < stack[-1][0]:
                stack.pop()
            current = stack[-1][1]
            if line.startswith("- "):
                item = line[2:].strip()
                current.append(parse_scalar(item))
                continue
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if value == "":
                next_container = [] if peek_next_list(path, raw_line) else {}
                current[key] = next_container
                stack.append((indent + 2, next_container))
            else:
                current[key] = parse_scalar(value)
    return result


def peek_next_list(path, current_line):
    lines = path.read_text(encoding="utf-8").splitlines()
    try:
        index = lines.index(current_line.rstrip("\n"))
    except ValueError:
        return False
    current_indent = len(current_line) - len(current_line.lstrip(" "))
    for next_line in lines[index + 1:]:
        if not next_line.strip() or next_line.lstrip().startswith("#"):
            continue
        next_indent = len(next_line) - len(next_line.lstrip(" "))
        return next_indent > current_indent and next_line.strip().startswith("- ")
    return False


def parse_scalar(value):
    if value == "[]":
        return []
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    return value.strip('"\'')


def validate_json_schema_file(path):
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return fail(f"{path}: invalid JSON schema: {exc}")
    for field in ["$schema", "title", "type"]:
        if field not in payload:
            return fail(f"{path}: missing schema field '{field}'")
    return True



def validate_workflow_configs(agent_ids):
    valid = True
    required_workflow = WORKFLOWS_DIR / "software-development.yaml"
    if not required_workflow.exists():
        return fail(f"missing required workflow config {required_workflow}")
    try:
        config = load_yaml(required_workflow)
    except Exception as exc:
        return fail(f"{required_workflow}: cannot parse YAML: {exc}")
    workflow = config.get("workflow", {})
    if workflow.get("id") != "software-development":
        valid = fail(f"{required_workflow}: workflow.id must be software-development") and valid
    for agent_id in workflow.get("required_agents", []):
        if agent_id not in agent_ids:
            valid = fail(f"{required_workflow}: unknown required agent '{agent_id}'") and valid
    stage_ids = [stage.get("id") for stage in workflow.get("stages", []) if isinstance(stage, dict)]
    for required_stage in ["intake", "classification", "planning", "routing", "execution", "review", "integration"]:
        if required_stage not in stage_ids:
            valid = fail(f"{required_workflow}: missing workflow stage '{required_stage}'") and valid
    for checkpoint in ["code_result_has_artifact", "code_result_has_generated_diff", "code_result_has_test_result", "code_result_has_final_summary"]:
        if checkpoint not in workflow.get("validation_checkpoints", []):
            valid = fail(f"{required_workflow}: missing validation checkpoint '{checkpoint}'") and valid
    if valid:
        print(f"valid: software-development -> {required_workflow}")
    return valid

def main():
    valid = True
    if not PERMISSIONS_FILE.exists():
        return 1 if fail(f"missing {PERMISSIONS_FILE}") else 1

    permissions = load_yaml(PERMISSIONS_FILE)
    policies = permissions.get("policies", {})
    tool_registry = permissions.get("tool_registry", {})
    model_profiles = {path.stem for path in MODELS_DIR.glob("*.yaml")}
    contract_files = {path.name for path in CONTRACTS_DIR.glob("*.schema.json")}

    for schema_file in CONTRACTS_DIR.glob("*.schema.json"):
        valid = validate_json_schema_file(schema_file) and valid

    for agent_id in REQUIRED_AGENTS:
        config_path = AGENTS_DIR / f"{agent_id}.yaml"
        if not config_path.exists():
            valid = fail(f"missing required agent config {config_path}") and valid
            continue
        try:
            config = load_yaml(config_path)
        except Exception as exc:
            valid = fail(f"{config_path}: cannot parse YAML: {exc}") and valid
            continue
        agent = config.get("agent", {})
        for field in REQUIRED_AGENT_FIELDS:
            if field not in agent:
                valid = fail(f"{config_path}: missing agent.{field}") and valid
        if agent.get("id") != agent_id:
            valid = fail(f"{config_path}: agent.id must be '{agent_id}'") and valid
        for prompt_field in ["prompt_template", "shared_policy_template"]:
            prompt_path = ROOT_DIR / str(agent.get(prompt_field, ""))
            if not prompt_path.exists() or not prompt_path.is_relative_to(PROMPTS_DIR):
                valid = fail(f"{config_path}: {prompt_field} points to missing or disallowed path {prompt_path}") and valid
        if agent.get("model_profile") not in model_profiles:
            valid = fail(f"{config_path}: unknown model_profile '{agent.get('model_profile')}'") and valid
        policy_name = agent.get("permission_policy")
        policy = policies.get(policy_name)
        if policy is None:
            valid = fail(f"{config_path}: unknown permission_policy '{policy_name}'") and valid
        agent_tools = set(agent.get("allowed_tools") or [])
        for tool_name in agent_tools:
            if tool_name not in tool_registry:
                valid = fail(f"{config_path}: disallowed or unknown tool '{tool_name}'") and valid
        if policy is not None and not agent_tools.issubset(set(policy.get("allowed_tools") or [])):
            valid = fail(f"{config_path}: allowed_tools exceed permission policy '{policy_name}'") and valid
        for contract_section in ["input_contract", "output_contract", "validation"]:
            section = agent.get(contract_section, {})
            schema_path = str(section.get("schema", ""))
            if schema_path and Path(schema_path).name not in contract_files:
                valid = fail(f"{config_path}: {contract_section}.schema does not exist: {schema_path}") and valid
        print(f"valid: {agent_id} -> {config_path}")

    valid = validate_workflow_configs(set(REQUIRED_AGENTS)) and valid

    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
