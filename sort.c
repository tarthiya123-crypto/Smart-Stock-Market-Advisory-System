#include "stock.h"

void sortStocks(
    Stock stocks[],
    int n
)
{
    Stock temp;

    for(int i=0;i<n-1;i++)
    {
        for(int j=0;j<n-i-1;j++)
        {
            if(
                stocks[j].finalScore <
                stocks[j+1].finalScore
            )
            {
                temp = stocks[j];

                stocks[j] =
                    stocks[j+1];

                stocks[j+1] =
                    temp;
            }
        }
    }
}