from typing import Dict, Any, List, Optional

class ICPFirmographicMatcher:
    """
    Evaluates B2B accounts against strict and weighted Ideal Customer Profile (ICP) criteria.
    Disqualifies non-viable prospects and tiers viable targets into Tier 1, Tier 2, and Tier 3.
    """
    DEFAULT_ICP_SPEC = {
        "allowed_geos": ["US", "CA", "UK", "EU", "AU"],
        "excluded_industries": ["Gambling", "Cryptocurrency Speculation", "Adult Content"],
        "headcount_range": {"min": 50, "max": 2000, "ideal_min": 100, "ideal_max": 500},
        "min_arr_usd": 5000000,
        "required_tech_keywords": ["Salesforce", "HubSpot", "Snowflake", "PostgreSQL"]
    }

    def __init__(self, icp_spec: Optional[Dict[str, Any]] = None):
        self.icp_spec = icp_spec if icp_spec else self.DEFAULT_ICP_SPEC

    def evaluate_icp_fit(self, account: Dict[str, Any]) -> Dict[str, Any]:
        disqualifications: List[str] = []
        score = 0
        notes: List[str] = []

        # 1. Hard Filter: Geography
        geo = account.get("country", "").upper()
        if geo and geo not in self.icp_spec.get("allowed_geos", []):
            disqualifications.append(f"Geo '{geo}' is outside target regions.")

        # 2. Hard Filter: Excluded Industries
        ind = account.get("industry", "")
        if ind in self.icp_spec.get("excluded_industries", []):
            disqualifications.append(f"Industry '{ind}' is on exclusion list.")

        # 3. Soft Filter: Headcount
        headcount = account.get("headcount", 0)
        hc_rule = self.icp_spec.get("headcount_range", {})
        if headcount < hc_rule.get("min", 0):
            notes.append(f"Headcount {headcount} below minimum {hc_rule.get('min')}.")
        elif headcount > hc_rule.get("max", 999999):
            notes.append(f"Headcount {headcount} above enterprise cap {hc_rule.get('max')}.")
        elif hc_rule.get("ideal_min", 0) <= headcount <= hc_rule.get("ideal_max", 999999):
            score += 40
            notes.append(f"Headcount {headcount} in ideal sweet-spot (+40 pts).")
        else:
            score += 25
            notes.append(f"Headcount {headcount} in acceptable boundary (+25 pts).")

        # 4. Soft Filter: ARR / Revenue
        arr = account.get("arr_usd", 0)
        min_arr = self.icp_spec.get("min_arr_usd", 0)
        if arr >= min_arr:
            score += 35
            notes.append(f"ARR ${arr:,} exceeds minimum ${min_arr:,} (+35 pts).")
        else:
            notes.append(f"ARR ${arr:,} below target ${min_arr:,}.")

        # 5. Soft Filter: Technographic Stack Match
        tech_stack = [t.lower() for t in account.get("technologies", [])]
        req_keys = self.icp_spec.get("required_tech_keywords", [])
        matched_keys = [k for k in req_keys if k.lower() in tech_stack]
        if matched_keys:
            bonus = min(25, len(matched_keys) * 10)
            score += bonus
            notes.append(f"Matched technographic assets {matched_keys} (+{bonus} pts).")

        # Tier assignment
        if disqualifications:
            tier = "Disqualified"
            is_qualified = False
        elif score >= 80:
            tier = "Tier 1 (High Priority ICP)"
            is_qualified = True
        elif score >= 50:
            tier = "Tier 2 (Qualified ICP)"
            is_qualified = True
        else:
            tier = "Tier 3 (Marginal Fit)"
            is_qualified = False

        return {
            "account_name": account.get("name", "Unknown"),
            "is_qualified": is_qualified,
            "tier": tier,
            "icp_fit_score": score,
            "disqualifications": disqualifications,
            "scoring_notes": notes
        }
