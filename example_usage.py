import json
from client import ICPFirmographicMatcher

def main():
    matcher = ICPFirmographicMatcher()
    candidate_account = {
        "name": "Prism Data Cloud",
        "country": "US",
        "industry": "Enterprise Software",
        "headcount": 180,
        "arr_usd": 12000000,
        "technologies": ["Salesforce", "Snowflake", "AWS"]
    }
    result = matcher.evaluate_icp_fit(candidate_account)
    print("ICP Fit Evaluation Result:")
    print(json.dumps(result, indent=2))
    assert result["is_qualified"] is True
    assert "Tier 1" in result["tier"]
    print("ICP matcher verification complete: PASS")

if __name__ == "__main__":
    main()
