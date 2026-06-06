#include <stdio.h>
#include <string.h>
#include "stock.h"

void calculateRisk(Stock *, int);
void allocatePortfolio(
    Stock[],
    int,
    double,
    int);
void sortStocks(
    Stock[],
    int);

int main()
{
    FILE *fp;

    fp = fopen(
        "market_data.csv",
        "r");

    if (fp == NULL)
    {
        printf("CSV not found\n");
        return 1;
    }

    Stock stocks[100];

    int count = 0;

    int userRisk;
    double amount;
    char horizon[20] = "MEDIUM";
    char firstLine[200];

    if (fgets(firstLine, sizeof(firstLine), fp) == NULL ||
        sscanf(firstLine, "%d,%lf,%19s", &userRisk, &amount, horizon) < 2)
    {
        printf("Invalid CSV input\n");
        fclose(fp);
        return 1;
    }

    printf(
        "Risk = %d\nAmount = %.2lf\nHorizon = %s\n",
        userRisk,
        amount,
        horizon);

    char header[200];

    fgets(
        header,
        sizeof(header),
        fp);

    while (
        fscanf(
            fp,
            "%[^,],%lf,%lf,%lf\n",
            stocks[count].name,
            &stocks[count].currentPrice,
            &stocks[count].growth,
            &stocks[count].volatility) == 4)
    {
        if (count >= 100)
        {
            printf("Maximum stock limit reached\n");
            break;
        }

        calculateRisk(
            &stocks[count],
            userRisk);

        double growthWeight;
        double riskWeight;
        double growthScore;
        growthScore=50+stocks[count].growth;
        if(growthScore>100){
            growthScore=100;
        }
        if(growthScore<0){
            growthScore=0;
        }
        if (strcmp(horizon, "SHORT") == 0)
        {
            growthWeight = 0.4;
            riskWeight = 0.6;
        }
        else if (strcmp(horizon, "MEDIUM") == 0)
        {
            growthWeight = 0.6;
            riskWeight = 0.4;
        }
        else
        {
            growthWeight = 0.8;
            riskWeight = 0.2;
        }

        stocks[count].finalScore =
            (growthWeight * growthScore +
             riskWeight * stocks[count].riskScore);

        printf(
            "\n%s\n",
            stocks[count].name);

        printf(
            "Growth = %.2lf\n",
            stocks[count].growth);

        printf(
            "GrowthScore = %.2lf\n",
            growthScore);

        printf(
            "RiskScore = %.2lf\n",
            stocks[count].riskScore);

        printf(
            "FinalScore = %.2lf\n",
            stocks[count].finalScore);

        count++;
    }

    fclose(fp);

    sortStocks(
        stocks,
        count);

    allocatePortfolio(
        stocks,
        count,
        amount,
        userRisk);

    FILE *out;

    out = fopen(
        "results.csv",
        "w");

    if (out == NULL)
    {
        printf("Could not create results.csv\n");
        return 1;
    }

    fprintf(
        out,
        "Stock,Score,RecommendedInvestment,Recommendation\n");

    for (int i = 0; i < count; i++)
    {
        if (stocks[i].finalScore >= 85)
        {
            strcpy(
                stocks[i].recommendation,
                "STRONG BUY");
        }

        else if (stocks[i].finalScore >= 70)
        {
            strcpy(
                stocks[i].recommendation,
                "BUY");
        }

        else if (stocks[i].finalScore >= 55)
        {
            strcpy(
                stocks[i].recommendation,
                "HOLD");
        }

        else if (stocks[i].finalScore >= 40)
        {
            strcpy(
                stocks[i].recommendation,
                "WATCH");
        }

        else
        {
            strcpy(
                stocks[i].recommendation,
                "AVOID");
        }

        fprintf(
            out,
            "%s,%.2lf,%.2lf,%s\n",
            stocks[i].name,
            stocks[i].finalScore,
            stocks[i].SuggestedInvestment,
            stocks[i].recommendation);
    }

    fclose(out);

    printf(
        "\nAnalysis Complete\n");

    return 0;
}
