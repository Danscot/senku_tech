import axios from 'axios';

export async function senku(message, client) {
  const remoteJid = message.key.remoteJid;
  const body =
    message.message?.extendedTextMessage?.text ||
    message.message?.conversation ||
    '';

  // Extract the user’s query (everything after ".ask")
  const parts = body.trim().split(/\s+/);
  const query = parts.slice(1).join(' ');
  if (!query) {
    await client.sendMessage(remoteJid, {
      text: '❌ Please provide a question. Usage: `.senku What is the capital of Cameroon?`'
    });
    return;
  }

  try {
    await client.sendMessage(remoteJid, {
      text: `🤖 Thinking…`,
      quoted: message
    });

    const apiUrl = `https://apis.davidcyriltech.my.id/ai/chatbot?query=${query}`;
    const { data } = await axios.get(apiUrl);

    if (!data.success || !data.result) {
      throw new Error('No answer received.');
    }

    // Send the AI’s reply
    await client.sendMessage(remoteJid, {
      text: `💬 Q: ${query}\n\n🤖 A: ${data.result}\n\n> Powered by Senku Tech`,
      quoted: message
    });

  } catch (err) {
    console.error('❌ Error in ask command:', err);
    await client.sendMessage(remoteJid, {
      text: `❌ Failed to get answer: ${err.message}`,
      quoted: message
    });
  }
}

export default senku;
