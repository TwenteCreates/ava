<template>
	<section>
		<!-- <header class="title">Ava</header> -->
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
			<div class="message-block typing" v-if="typing">
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
				<input type="text" v-model="reply" placeholder="Enter a message...">
				<button type="submit">
					<font-awesome-icon icon="arrow-right" />
				</button>
			</form>
		</footer>
	</section>
</template>

<script>
import FontAwesomeIcon from "@fortawesome/vue-fontawesome";
export default {
	mounted() {
		this.messages = this.$store.state.messages;
		if (this.messages.length === 0) {
			this.botSays(`Hi 👋`);
			this.botSays(`I'm Ava from Talanx`);
			this.botSays(`How can I help?`);
		}
	},
	data: () => {
		return {
			typing: false,
			reply: "",
			messages: []
		};
	},
	methods: {
		botSays(text) {
			if (this.messages.length > 0) {
				this.messages[this.messages.length - 1].next = "sender-1";
			}
			this.messages.push({
				sender: "sender-1",
				text: text,
				previous:
					this.messages.length > 0
						? this.messages[this.messages.length - 1].sender
						: "unknown"
			});
		},
		sendMessage() {
			if (!this.reply || !this.reply.trim()) return;
			if (this.reply.toLowerCase() === "clear") {
				this.messages = [];
				this.reply = "";
				this.$store.commit("update", this.messages);
				location.reload();
				return;
			}
			if (this.messages.length > 0) {
				this.messages[this.messages.length - 1].next = "sender-2";
			}
			this.messages.push({
				sender: "sender-2",
				text: this.reply,
				previous:
					this.messages.length > 0
						? this.messages[this.messages.length - 1].sender
						: "unknown"
			});
			this.reply = "";
			this.$store.commit("update", this.messages);
			setTimeout(() => {
				this.$el.querySelector("main").scrollTop = this.$el.querySelector(
					"main"
				).scrollHeight;
			}, 1);
		}
	},
	components: {
		FontAwesomeIcon
	}
};
</script>

<style lang="scss" scoped>
main {
	padding: 1.5rem;
}

.message-block {
	.message {
		background-color: #fff;
		display: inline-block;
		padding: 0.75rem 1rem;
		box-shadow: 0 0.5rem 1rem rgba(0, 100, 100, 0.1);
		border-radius: 25px;
		.emoji {
			font-size: 50%;
			display: inline-block;
			margin-left: 0.65rem;
			transform: scale(2) translateY(-0.075rem);
		}
	}
	.sender {
		float: left;
		margin-right: 0.5rem;
		img {
			width: 25px;
			height: 25px;
			border-radius: 15px;
		}
	}
	&.sender-2 {
		.message {
			background-color: #cb0056;
			color: #fff;
		}
	}
	&.sender-1 + .sender-2 {
		margin-top: 1.5rem;
	}
	&.sender-2 + .sender-1 {
		margin-top: 1.5rem;
	}
	&.sender-2 + .sender-2 {
		margin-top: 0.25rem;
		.sender img {
			visibility: hidden;
		}
	}
	&.sender-1 + .sender-1 {
		margin-top: 0.25rem;
		.sender img {
			visibility: hidden;
		}
	}
	&.sender-2 {
		> div {
			display: flex;
			justify-content: flex-end;
		}
		.sender {
			float: right;
			margin-right: 0;
			margin-left: 0.5rem;
		}
	}
	&.sender-1.next-sender-1 {
		.message {
			border-bottom-left-radius: 15px;
		}
		+ div {
			.message {
				border-top-left-radius: 15px;
			}
		}
	}
	&.sender-2.next-sender-2 {
		.message {
			border-bottom-right-radius: 15px;
		}
		+ div {
			.message {
				border-top-right-radius: 15px;
			}
		}
	}
	&.sender-1.next-sender-1.previous-sender-1,
	&.sender-2.next-sender-2.previous-sender-2 {
		.message {
			border-top-right-radius: 15px;
			border-bottom-right-radius: 15px;
		}
	}
	&.typing {
		.ellipsis-1 {
			display: inline-block;
			animation: pulse 1s infinite;
			animation-delay: 0;
		}
		.ellipsis-2 {
			display: inline-block;
			animation: pulse 1s infinite;
			animation-delay: 333ms;
		}
		.ellipsis-3 {
			display: inline-block;
			animation: pulse 1s infinite;
			animation-delay: 666ms;
		}
	}
	&.meta {
		font-size: 85%;
		margin: 1.5rem 0;
		text-align: center;
		opacity: 0.75;
	}
}

@keyframes pulse {
	0% {
		transform: translateY(0);
		opacity: 1;
	}
	50% {
		opacity: 0.25;
		transform: translateY(-5px);
	}
	100% {
		transform: translateY(0);
		opacity: 1;
	}
}

.reply-box {
	z-index: 1000;
	box-shadow: 0 -0.5rem 1rem rgba(0, 100, 100, 0.05);
	form {
		display: flex;
		justify-content: space-between;
	}
	input,
	button {
		border: none;
		padding: 1rem;
	}
	button {
		svg {
			color: #cb0056;
			transform: scale(1.5) translateX(-3px);
		}
	}
	input {
		width: 100%;
	}
}
</style>
