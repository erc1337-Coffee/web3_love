// Here's the link of the discord.js documentation : https://discordjs.guide/

// Create a discord bot here https://discord.com/developers/applications
// Then paste its token in the config.json file

/*

	NOTE: There is 2 steps here. 
		
		1. You must register your bot's commands to the 
		discord server (discord server are called guilds in the documentation). 
		-> You'll only have to re-run this file each time you add or remove commands !
	
		2. Then, you can start this file which will run the bot. 
*/

// Import all the needed libraries and the token which is in config.json
const { Client, Intents } = require('discord.js');
const { guildId, clientId, token } = require('./config.json');

// Create a new client instance
const client = new Client({ intents: [Intents.FLAGS.GUILDS] });

// This code is executed only once when the script starts
client.once('ready', () => {
	console.log('Ready!');
});

// Here is the handler for commands
client.on('interactionCreate', async interaction => {
	// If the user sent an invalid command, then exit
	if (!interaction.isCommand()) return;

	const { commandName } = interaction;

	// Not very pretty, but we'll do if statements
	// to get the user to the wanted command
	// After understanding this code, you should re-organize
	// commands execution in separate js files.
	if (commandName === 'help') {
		// We create a beautiful help menu
		var help_menu_content = `
This is a simple help menu :)

**🦖    /echo (text) :**
\`The bot will show the message you sent.\`

**🪙    /help :**
\`This beautiful help menu.\`
		`

		// Reply to the user
		await interaction.reply(help_menu_content);
	} else if (commandName === 'echo') {
		// To get the passed argument, use interaction.options.get()
		// in register_commands.js we created the echo command with the following
		// input :  option.setName('message')
		// That's why we get the argument by using interaction.options.get("message")
		var user_input = interaction.options.get("message").value

		// Create the answer
		var echo_answer = `🦖🪙    ${interaction.user.username} sent: ${user_input}` ;

		// Reply to the user
		await interaction.reply(echo_answer);
	}
});


// Start the bot
client.login(token);
