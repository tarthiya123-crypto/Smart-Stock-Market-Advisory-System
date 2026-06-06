#ifndef STOCK_H
#define STOCK_H

typedef struct
{
    char name[50];

    double confidence;

    double currentPrice;

    double growth;

    double volatility;

    double riskScore;

    double finalScore;

    double SuggestedInvestment;

    char recommendation[20];

} Stock;

#endif