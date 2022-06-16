const { SlashCommandBuilder } = require('@discordjs/builders');
const { REST } = require('@discordjs/rest');
const { Routes } = require('discord-api-types/v9');
const { clientId, guildId, token } = require('./config.json');
const rest = new REST({ version: '9' }).setToken(token);

// We then register our commands 
const commands = [
	// Register a help command, which takes no argument
	new SlashCommandBuilder().setName('help').setDescription('Show a beautiful help menu.'),
	// Register a echo command, the user will have to supply a message
	new SlashCommandBuilder().setName('echo').setDescription('Echo what the user sent.').addStringOption(option => option.setName('message').setDescription('The user message which will be echoed.')),
]
.map(command => command.toJSON());

// Push the commands to the guild specified in config.json
rest.put(Routes.applicationGuildCommands(clientId, guildId), { body: commands })
	.then(() => console.log('Successfully registered application commands.'))
	.catch(console.error);
