install.packages("forecast")
library(forecast)

data <- read.csv("recording1.csv")

ts_data <- ts(data$sum, start = 1, frequency = 1)

# Split data
train <- window(ts_data, end = 24)
test <- window(ts_data, start = 25, end = 30)

# Fit ARIMA 
arima_model <- arima(train, order = c(2,0,0))
forecast_values <- forecast(arima_model, h = 15)

plot(ts_data, main = "ARIMA Forecast", xlab = "Time (minutes)", ylab = "Sum", xlim = c(1,45))
lines(test, col = "blue")

lines(forecast_values$mean, col = "orange")

# legend 
legend("topright", legend = c("Actual Data", "Test Data", "Forecast"), 
       col = c("black", "blue", "orange"), lty = c(1, 1, 1), cex = 0.8)

# write csv
forecast_df <- cbind(actual_data = ts_data, forecasted_data = forecast_values$mean)
write.csv(forecast_df, "forecast_results.csv", row.names = FALSE)
