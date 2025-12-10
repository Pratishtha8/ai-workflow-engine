# Async node implementations for Code Review workflow
# These functions are intentionally simple rule-based heuristics suitable for interviews.
import asyncio
from typing import Dict

async def extract_functions(state: Dict):
    await asyncio.sleep(0)  # placeholder for I/O
    code = state.get("code", "")
    funcs = []
    for line in code.splitlines():
        line = line.strip()
        if line.startswith("def "):
            name = line.split("(")[0].replace("def ", "").strip()
            funcs.append(name)
    state['functions'] = funcs or ['<no_function_found>']
    state.setdefault('logs', []).append(f'extract_functions -> {len(state["functions"])} found')
    return state

async def check_complexity(state: Dict):
    await asyncio.sleep(0)
    funcs = state.get('functions', [])
    complexity = 0
    if funcs and funcs != ['<no_function_found>']:
        complexity = sum(len(f) for f in funcs) // max(1, len(funcs)) + 3
    else:
        complexity = 5
    state['complexity'] = complexity
    state.setdefault('logs', []).append(f'check_complexity -> {complexity}')
    return state

async def detect_issues(state: Dict):
    await asyncio.sleep(0)
    issues = []
    code = state.get('code', '')
    if 'print(' in code and 'logging' not in code:
        issues.append('use-logging-instead-of-print')
    for i, line in enumerate(code.splitlines(), start=1):
        if len(line) > 120:
            issues.append(f'long-line:{i}')
    if '\t' in code or '    ' in code:
        issues.append('possible-deep-nesting')
    state['issues'] = issues
    state.setdefault('logs', []).append(f'detect_issues -> {len(issues)}')
    return state

async def suggest_improvements(state: Dict):
    await asyncio.sleep(0)
    suggestions = []
    complexity = state.get('complexity', 0)
    issues = state.get('issues', [])
    if complexity > 6:
        suggestions.append('refactor:break-into-smaller-functions')
    if any(i.startswith('long-line') for i in issues):
        suggestions.append('wrap-or-shorter-lines')
    if 'use-logging-instead-of-print' in issues:
        suggestions.append('replace-print-with-logging')
    if 'possible-deep-nesting' in issues:
        suggestions.append('reduce-nesting')
    state.setdefault('suggestions', []).extend(suggestions)
    # simulate an improvement so loop can converge
    state['complexity'] = max(0, state.get('complexity', 0) - 1)
    state.setdefault('logs', []).append(f'suggest_improvements -> {len(suggestions)}')
    return state

async def compute_quality(state: Dict):
    await asyncio.sleep(0)
    complexity = state.get('complexity', 0)
    issues = state.get('issues', [])
    score = max(0, 10 - complexity - len(issues))
    state['quality_score'] = score
    state.setdefault('logs', []).append(f'compute_quality -> {score}')
    return state
