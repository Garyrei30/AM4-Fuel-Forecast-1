# AM4-Fuel-Forecast
AM4-Fuel-Forecast is a Discord bot specifically designed for the Regius Alliance in the Airline Manager 4 game. The bot provides fuel and CO2 price forecasts for the game and is tailored to work on the Regius Alliance server. It utilizes a database to store and retrieve relevant data for generating forecasts. The bot includes two main commands: !fuel and !fuel daily.

## Features
### !fuel
The !fuel command retrieves the forecast for the next 5 hours of fuel and CO2 prices that will be in the game. The bot fetches data from the database, formats it into an aesthetically pleasing embed message with emojis, and sends it in the same channel where the command was invoked. The embed message also highlights when the prices are cheap giving a visual representation.

### !fuel daily
The !fuel daily command provides daily updates on Fuel and CO2 prices. It informs users about the time periods when the prices are expected to be cheap, i.e., less than $550 for Fuel and $130 for CO2. Similar to the !fuel command, the bot generates an embed message with the forecasted prices and time information. The embed message also includes a feature to display the user's local time, allowing them to check the forecast according to their device's time.

### Data Synchronization
The Discord bot continuously monitors a designated channel for current Fuel Prices. If the prices in the channel differ from the values stored in the database, the bot automatically updates the database with the latest prices. This ensures that the forecasts provided by the bot remain accurate and up to date.

## Contributing

Contributions to the AM4-Fuel-Forecast bot are welcome. If you have any suggestions, bug fixes, or improvements, please follow these steps:

1. Fork the repository.

2. Create a new branch:
   ```
   git checkout -b my-feature
   ```

3. Make the necessary changes and commit them:
   ```
   git commit -m "Add my feature"
   ```

4. Push the changes to your forked repository:
   ```
   git push origin my-feature
   ```

5. Open a pull request on the main repository, describing your changes in detail.

## License

The AM4-Fuel-Forecast bot is released under the [MIT License](LICENSE).

## Acknowledgments

- The developers of Airline Manager 4 for providing the game that inspired this project.
- The creators of the Discord API and Flask framework for enabling the bot's functionality.
- [OpenAI](https://openai.com/) for developing GPT-3.5, the language model used to help in creation of this readme file.
