from .planner import plan_intent
from .tools import FinancialTools

class FinancialAgent:

    def __init__(self, data_frames):
        self.tools = FinancialTools(data_frames)

    def run(self, query: str):
        
        plan = plan_intent(query)
        intent = plan["intent"]
        month = plan["month"]
        
        if intent == "get_revenue_vs_budget":
            result = self.tools.get_revenue_vs_budget(month_str=month)
        elif intent == "get_gross_margin_trend":
            result = self.tools.get_gross_margin_trend()
        elif intent == "get_opex_breakdown":
            result = self.tools.get_opex_breakdown(month_str=month)
        elif intent == "get_cash_runway":
            result = self.tools.get_cash_runway()
        elif intent == "get_ebitda_proxy":
            result = self.tools.get_ebitda_proxy(month_str=month)
        else:
            result = {
                "text": "I can answer questions about `Revenue vs Budget`, `Gross Margin`, `Opex`, `EBITDA`, and `Cash Runway`. Please try one of those.",
                "chart": None
            }
            
        return result