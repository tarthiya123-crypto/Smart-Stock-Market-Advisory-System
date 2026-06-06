#include "stock.h"

void calculateRisk(
    Stock *stock,
    int userRisk
)
{
    double stockRisk;

    stockRisk =
        stock->volatility * 20;

    if(stockRisk > 100)
        stockRisk = 100;

    stock->riskScore =
        100 -
        (
            stockRisk > userRisk ?
            stockRisk - userRisk :
            userRisk - stockRisk
        );

    if(stock->riskScore < 0)
        stock->riskScore = 0;
}