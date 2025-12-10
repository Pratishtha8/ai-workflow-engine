from app.engine.nodes import (
    extract_functions,
    check_complexity,
    detect_issues,
    suggest_improvements,
    compute_quality
)

def get_code_review_workflow(threshold: int = 7):
    nodes = {
        'extract_functions': extract_functions,
        'check_complexity': check_complexity,
        'detect_issues': detect_issues,
        'suggest_improvements': suggest_improvements,
        'compute_quality': compute_quality
    }
    edges = {
        'extract_functions': 'check_complexity',
        'check_complexity': 'detect_issues',
        'detect_issues': 'suggest_improvements',
        'suggest_improvements': 'compute_quality',
        'compute_quality': None
    }
    return {'nodes': nodes, 'edges': edges, 'start': 'extract_functions', 'threshold': threshold}
