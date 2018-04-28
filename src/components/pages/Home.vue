<template>
	<section>
		<header class="title">
			Chat
		</header>
		<main class="main-chat">
			<div v-for="(message, index) in messages" :key="`message${index}`" v-bind:class="`message-block ${message.sender} next-${message.next || 'none'} previous-${message.previous || 'none'}`">
				<div v-if="message.sender === `meta`" class="message-meta">
					<div class="details">{{message.text}}</div>
				</div>
				<div v-else-if="message.sender === `sender-1`" class="message-content">
					<div class="sender">
						<img alt="Sender's Avatar" src="/bot.svg">
						</div>
					<div class="message">{{message.text}}</div>
				</div>
				<div v-else class="message-content">
					<div class="message">{{message.text}}</div>
					<div class="sender">
						<img alt="Sender's Avatar" src="https://randomuser.me/api/portraits/men/14.jpg">
					</div>
				</div>
			</div>
			<div class="message-block typing">
				<div class="message-content">
					<div class="sender">
						<img alt="Sender's Avatar" src="https://randomuser.me/api/portraits/women/14.jpg">
						</div>
					<div class="message">
						<span class="ellipsis-1">&bullet;</span>
						<span class="ellipsis-2">&bullet;</span>
						<span class="ellipsis-3">&bullet;</span>
					</div>
				</div>
			</div>
		</main>
		<footer class="reply-box">
			<form @submit.prevent="sendMessage">
				<input type="text" v-model="reply">
				<button type="submit">Send</button>
			</form>
		</footer>
	</section>
</template>

<script>
export default {
	data: () => {
		return {
			reply: "",
			messages: [
				{
					sender: "sender-1",
					text: `Hi 👋`,
					next: "sender-1"
				},
				{
					sender: "sender-1",
					text: `How are you doing?`,
					next: "sender-2",
					previous: "sender-1"
				},
				{
					sender: "sender-2",
					text: `I'm doing great, how are you?`,
					next: "sender-1",
					previous: "sender-1"
				},
				{
					sender: "sender-1",
					text: `Awesome!`,
					next: "sender-2",
					previous: "sender-2"
				},
				{
					sender: "sender-2",
					text: `Cool!`,
					next: "sender-2",
					previous: "sender-1"
				},
				{
					sender: "sender-2",
					text: `So, tell me something...`,
					next: "sender-2",
					previous: "sender-2"
				},
				{
					sender: "sender-2",
					text: `What can you do?`,
					previous: "sender-2",
					next: "sender-1"
				},
				{
					sender: "meta",
					text: `Isabella has joined the conversation`
				}
			]
		};
	},
	methods: {
		sendMessage() {
			this.messages[this.messages.length - 1].next = "sender-2";
			this.messages.push({
				sender: "sender-2",
				text: this.reply,
				previous: this.messages[this.messages.length - 1].sender
			});
			this.reply = "";
			setTimeout(() => {
				this.$el.querySelector("main").scrollTop = this.$el.querySelector(
					"main"
				).scrollHeight;
			}, 1);
		}
	}
};
</script>
