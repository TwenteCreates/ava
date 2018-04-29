<template>
	<section>
		<header>Claim Approval</header>
		<main class="main-chat">
			<h3 style="margin-top: 0">Customer information</h3>
			<div class="card-row">
				<div class="card-icon">
					<font-awesome-icon icon="user" />
				</div>
				<div class="card">
					<div><strong>Name</strong></div>
					<div>Anand Chowdhary</div>
				</div>
			</div>
			<div class="card-row">
				<div class="card-icon">
					<font-awesome-icon icon="car" />
				</div>
				<div class="card">
					<div><strong>Insurance type</strong></div>
					<div>{{data.data.insurance_claim}} insurance</div>
				</div>
			</div>
			<div class="card-row">
				<div class="card-icon">
					<font-awesome-icon icon="calendar" />
				</div>
				<div class="card">
					<div><strong>Date &amp; time</strong></div>
					<div>{{data.data.when_happened}}</div>
				</div>
			</div>
			<div class="card-row">
				<div class="card-icon">
					<font-awesome-icon icon="location-arrow" />
				</div>
				<div class="card">
					<div><strong>Location</strong></div>
					<div>{{data.data.place_name}}</div>
				</div>
			</div>
			<h3>Actions</h3>
			<div class="actions" style="margin-bottom: 2rem">
				<button class="action-button" @click="conversationVisible = !conversationVisible">
					<font-awesome-icon icon="comments" />
					<span>View Conversation</span>
				</button>
				<button class="action-button">
					<font-awesome-icon icon="comments" />
					<span>Start Talking</span>
				</button>
			</div>
			<div v-if="conversationVisible" v-for="(message, index) in messages" :key="`message${index}`" v-bind:class="`message-block ${message.sender} next-${message.next || 'none'} previous-${message.previous || 'none'} class-${message.class || 'none'}`">
				<div v-if="message.sender === `meta`" class="message-meta">
					<div class="details">{{message.text}}</div>
				</div>
				<div v-else-if="message.sender === `sender-3`" class="message-content">
					<div class="message">
						<div class="message-inner">{{message.text}}</div></div>
					<div class="sender">
						<img alt="Sender's Avatar" :src="message.avatar">
					</div>
				</div>
				<div v-else class="message-content">
					<div class="sender">
						<img alt="Sender's Avatar" :src="message.avatar">
					</div>
					<div class="message">
						<div class="message-inner">{{message.text}}</div></div>
				</div>
			</div>
		</main>
		<footer v-if="joinConversation">
			<transition name="fade" mode="out-in">
				<div class="options" v-if="options.length > 0">
					<ul>
						<li v-for="(option, id) in options" :key="`option_${id}`">
							<button @click="animateButton(option)">{{option}}</button>
						</li>
					</ul>
				</div>
			</transition>
			<div class="reply-box">
				<form @submit.prevent="sendMessage">
					<input type="text" v-model="reply" placeholder="Enter a message...">
					<button type="button" v-if="!speaking" @click="startSpeech">
						<font-awesome-icon icon="microphone" fixed-width />
					</button>
					<button type="button" v-else>
						<font-awesome-icon icon="signal" fixed-width />
					</button>
					<button type="submit">
						<font-awesome-icon icon="arrow-right" fixed-width />
					</button>
				</form>
			</div>
		</footer>
	</section>
</template>

<script>
import firebase from "firebase";
import FontAwesomeIcon from "@fortawesome/vue-fontawesome";
import sentenceCase from "sentence-case";
const database = firebase.database();
function getOffset(el) {
	var _x = 0;
	var _y = 0;
	while (el && !isNaN(el.offsetLeft) && !isNaN(el.offsetTop)) {
		_x += el.offsetLeft - el.scrollLeft;
		_y += el.offsetTop - el.scrollTop;
		el = el.offsetParent;
	}
	return { top: _y, left: _x };
}
export default {
	mounted() {
		const messages = firebase.database().ref("/");
		messages.once("value").then(snapshot => {
			this.data = snapshot.val() || {};
			this.messages = snapshot.val().conversation || [];
		});
		messages.on("value", snapshot => {
			if (snapshot.val()) {
				this.data = snapshot.val();
				this.messages = snapshot.val().conversation || [];
			}
		});
	},
	data: () => {
		return {
			data: {},
			typing: false,
			reply: "",
			speaking: false,
			messages: [],
			voice: null,
			options: [],
			nextMessages: [],
			currentQ: null,
			conversationVisible: false,
			joinConversation: false
		};
	},
	methods: {
		saveMessages() {
			database.ref("/conversation").set(this.messages);
		},
		startSpeech() {
			if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
				this.speaking = true;
				const recognition = new webkitSpeechRecognition() || new SpeechRecognition();
				recognition.start();
				recognition.addEventListener("result", text => {
					recognition.stop();
					this.sendMessage(sentenceCase(text.results[0][0].transcript));
					this.speaking = false;
				});
			}
		},
		sendMessage(reply = this.reply) {
			if (typeof reply !== "string") reply = this.reply;
			this.reply = "";
			if (!reply || !reply.trim()) return;
			if (reply.toLowerCase() === "clear") {
				this.messages = [];
				this.saveMessages();
				location.reload();
				return;
			}
			if (this.messages.length > 0) {
				this.messages[this.messages.length - 1].next = "sender-3";
			}
			this.messages.push({
				sender: "sender-3",
				text: reply,
				avatar: "/manager.png",
				previous:
					this.messages.length > 0
						? this.messages[this.messages.length - 1].sender
						: "unknown"
			});
			this.saveMessages();
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
	.message-content {
		display: flex;
		justify-content: flex-start;
	}
	.message {
		flex: 1 0 0;
		.message-inner {
			background-color: #ffffff;
			display: inline-block;
			padding: 0.75rem 1rem;
			box-shadow: 0 0.5rem 1rem rgba(0, 100, 100, 0.1);
			border-radius: 25px;
		}
		.emoji {
			font-size: 50%;
			display: inline-block;
			margin-left: 0.65rem;
			transform: scale(2) translateY(-0.075rem);
		}
	}
	.sender {
		margin-right: 0.5rem;
		width: 25px;
		img {
			width: 25px;
			height: 25px;
			border-radius: 15px;
		}
	}
	&.sender-3 {
		.message-inner {
			background-color: #3498db;
			color: #fff;
		}
	}
	&.sender-1 + .sender-3,
	&.sender-1 + .sender-2,
	&.sender-2 + .sender-1,
	&.sender-2 + .sender-3,
	&.sender-3 + .sender-1,
	&.sender-3 + .sender-2 {
		margin-top: 1.5rem;
	}
	&.sender-3 + .sender-3 {
		margin-top: 0.25rem;
		.sender img {
			visibility: hidden;
		}
	}
	&.sender-3 + .sender-3 {
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
	&.sender-3 {
		.message {
			display: flex;
			justify-content: flex-end;
		}
		.sender {
			margin-right: 0;
			margin-left: 0.5rem;
		}
	}
	&.sender-1.next-sender-1,
	&.sender-3.next-sender-3 {
		.message-inner {
			border-bottom-left-radius: 15px;
		}
		+ div {
			.message-inner {
				border-top-left-radius: 15px;
			}
		}
	}
	&.sender-3.next-sender-3 {
		.message-inner {
			border-bottom-right-radius: 15px;
		}
		+ div {
			.message-inner {
				border-top-right-radius: 15px;
			}
		}
	}
	&.sender-1.next-sender-1.previous-sender-1,
	&.sender-3.next-sender-3.previous-sender-3,
	&.sender-3.next-sender-3.previous-sender-3 {
		.message-inner {
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

footer {
	z-index: 1000;
}
.reply-box {
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
			color: #3498db;
			transform: scale(1.5);
		}
	}
	input {
		width: 100%;
	}
}
.options {
	position: relative;
	&::before {
		content: "";
		position: absolute;
		left: 0;
		right: 0;
		height: 2rem;
		top: -2rem;
		background: linear-gradient(transparent, #f3f6f7);
	}
	background: #f3f6f7;
	ul {
		transition: 500ms;
		margin: 0;
		padding: 0;
		list-style: none;
		white-space: nowrap;
		width: 100%;
		overflow-x: auto;
		li {
			display: inline-block;
			margin: 0;
			padding: 5px 0 1rem 1rem;
			&:last-of-type {
				padding-right: 1rem;
			}
			button {
				background-color: #3498db;
				color: #fff;
				border: none;
				padding: 0.75rem 1rem;
				border-radius: 25px;
			}
		}
	}
}
.class-temp {
	.message {
		visibility: hidden;
	}
	.sender img {
		opacity: 0;
		transition: 500ms;
	}
}
input {
	outline: none;
}
.card {
	background-color: #fff;
	box-shadow: 0 0.5rem 1rem rgba(0, 100, 100, 0.1);
	padding: 1rem;
	border-radius: 15px;
	flex: 1 0 0;
}
.card-row {
	display: flex;
	+ .card-row {
		margin-top: 1rem;
	}
	.card-icon {
		background-color: #aaa;
		border-radius: 15px;
		margin-right: 1rem;
		font-size: 150%;
		padding: 0 1rem;
		display: flex;
		flex-direction: column;
		justify-content: center;
		color: #fff;
	}
	&:nth-of-type(1) .card-icon {
		background-color: #cb0056;
	}
	&:nth-of-type(2) .card-icon {
		background-color: #3498db;
	}
	&:nth-of-type(3) .card-icon {
		background-color: #2ecc71;
	}
	&:nth-of-type(4) .card-icon {
		background-color: #f39c12;
	}
}
.action-button {
	width: 100%;
	padding: 0.75rem 0;
	border-radius: 15px;
	font-size: 110%;
	background-color: #666;
	color: #fff;
	svg {
		margin-right: 0.5rem;
	}
	+ .action-button {
		margin-top: 0.75rem;
	}
}
</style>
