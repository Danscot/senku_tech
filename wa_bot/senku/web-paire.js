
import bot from './utils/connector.js'

import handleIncomingMessage from './events/messageHandler.js';

const number = process.env.NUMBER;

const SESSION_DURATION_SEC = parseInt(process.env.SESSION_DURATION_SEC || "172800"); // default 2 days

async function launchBot() {

  console.log(`Starting bot for ${SESSION_DURATION_SEC} seconds`);

  const session = await bot.startSession(number, handleIncomingMessage, true);

  setTimeout(async () => {

    console.log(`Bot session expired for ${number} at ${new Date().toLocaleString()}`);

    try {

      await bot.removeSession(number);

      console.log("Bot stopped successfully.");

    } catch (err) {

      console.error("Error stopping bot:", err);
    }

  }, SESSION_DURATION_SEC * 1000);
}

launchBot();

