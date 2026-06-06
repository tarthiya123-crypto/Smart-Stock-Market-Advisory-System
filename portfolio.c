#include "stock.h"

void allocatePortfolio(
    Stock stocks[],
    int n,
    double amount,
    int userRisk
)
{
    for(int i = 0; i < n; i++)
    {
        double riskMatch;

        /* Risk score already lies roughly between 0 and 100 */

        riskMatch = stocks[i].riskScore;

        stocks[i].SuggestedInvestment =
            amount *
            (stocks[i].finalScore / 100.0) *
            (riskMatch / 100.0);

        /* Safety limits */

        if(stocks[i].SuggestedInvestment > amount)
        {
            stocks[i].SuggestedInvestment = amount;
        }

        if(stocks[i].SuggestedInvestment < 0)
        {
            stocks[i].SuggestedInvestment = 0;
        }
    }
}