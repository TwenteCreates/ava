<template>
	<section>
		<header>Claim Approval</header>
		<main class="main-chat">
			<h3 style="margin-top: 0">Claim information</h3>
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
					<div>{{(data.data || {}).insurance_claim || "Unknown"}} insurance</div>
				</div>
			</div>
			<div class="card-row">
				<div class="card-icon">
					<font-awesome-icon icon="calendar" />
				</div>
				<div class="card">
					<div><strong>Date &amp; time</strong></div>
					<div>{{(data.data || {}).when_happened || "Unknown"}}</div>
				</div>
			</div>
			<div class="card-row">
				<div class="card-icon">
					<font-awesome-icon icon="smile" />
				</div>
				<div class="card">
					<div><strong>Sentiment</strong></div>
					<div v-for="(one, id) in sentiment" :key="`sentiment_${id}`">
						{{one}}
					</div>
				</div>
			</div>
			<div class="card-row">
				<div class="card-icon">
					<font-awesome-icon icon="location-arrow" />
				</div>
				<div class="card">
					<a target="_blank" :href="`https://www.google.com/maps?q=${encodeURIComponent((data.data || {}).place_name)}`">
						<img alt="Map" v-if="(data.data || {}).place_name" :src="`https://maps.googleapis.com/maps/api/staticmap?key=AIzaSyCuiZevIb1G87KAoLRSECEdWNBQ06JCMjU&center=${encodeURIComponent((data.data || {}).place_name || 'Unknown')}&size=640x350&zoom=13`">
					</a>
					<div><strong>Location</strong></div>
					<div>{{(data.data || {}).place_name || "Unknown"}}</div>
				</div>
			</div>
			<h3>Actions</h3>
			<button class="action-button" @click="conversationVisible = !conversationVisible">
				<font-awesome-icon icon="comments" />
				<span><span v-if="!conversationVisible">Show</span><span v-else>Hide</span><span> Conversation</span></span>
			</button>
			<button class="action-button" @click="startTalking" v-if="!joinConversation">
				<font-awesome-icon icon="comment" />
				<span>Start Talking</span>
			</button>
			<div v-if="conversationVisible" style="margin: 2rem 0">
				<div v-for="(message, index) in messages" :key="`message${index}`" v-bind:class="`message-block ${message.sender} next-${message.next || 'none'} previous-${message.previous || 'none'} class-${message.class || 'none'}`">
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
							<div class="message-inner" v-if="!message.text.includes(`IMAGE_URL|`)">{{message.text}}</div>
							<div class="message-inner inline-image" v-else>
								<div v-if="imageUrl"><img alt="Uploaded image" :src="imageUrl"></div>
								<div v-else><font-awesome-icon icon="sync" spin /> &nbsp;Loading...</div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div class="yes-no" v-if="undecided" style="margin-top: 1rem">
				<button class="action-button" @click="decline">
					<font-awesome-icon icon="times" />
					<span>Decline</span>
				</button>
				<button class="action-button" @click="approve">
					<font-awesome-icon icon="check" />
					<span>Approve</span>
				</button>
			</div>
		</main>
		<footer v-if="joinConversation">
			<transition name="fade" mode="out-in">
				<div class="options" v-if="options.length > 0">
					<ul>
						<li v-for="(option, id) in options" :key="`option_${id}`">
							<button @click="smartSend(option, id)">{{option}}</button>
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
	while (el && !isNaN(el.offsetLeft) && !isNaN(eloffsetTop)) {
		_x += el.offsetLeft - el.scrollLeft;
		_y += el.offsetTop - el.scrollTop;
		el = el.offsetParent;
	}
	return { top: _y, left: _x };
}
export default {
	mounted() {
		const messages = firebase.database().ref(`/${localStorage.sessionID}/`);
		messages.once("value").then(snapshot => {
			this.data = snapshot.val() || {};
			this.messages = snapshot.val().conversation || [];
			this.messages.forEach(message => {
				if (message.text === "Isabella has joined the conversation") {
					this.joinConversation = true;
					this.conversationVisible = true;
				}
			});
		});
		messages.on("value", snapshot => {
			if (snapshot.val()) {
				this.data = snapshot.val();
				this.messages = (snapshot.val() || {}).conversation || [];
				let sentimentMessage = "";
				this.messages.forEach(message => {
					if (
						[
							"I've approved your request",
							"I'm sorry, but I've declined your request"
						].includes(message.text)
					) {
						this.undecided = false;
					}
					if (message.text.includes("IMAGE_URL|")) {
						if (!this.imageUrl) {
							const file = firebase
								.storage()
								.ref(message.text.replace("IMAGE_URL|", ""));
							file
								.getDownloadURL()
								.then(url => {
									this.imageUrl = url;
								})
								.catch(() => {});
						}
					}
					if (message.sender === "sender-2") {
						sentimentMessage += message.text + ". ";
					}
				});
				if (sentimentMessage) {
					fetch(
						`https://myapp-thankful-chimpanzee.cfapps.eu10.hana.ondemand.com/analyze?text=${encodeURIComponent(
							sentimentMessage
						)}`
					)
						.then(response => response.json())
						.then(json => {
							this.sentiment = [
								parseInt(json.results.friendly.score * 100) + "%  friendly",
								parseInt(json.results.appreciative.score * 100) + "%  appreciative",
								parseInt(json.results.authoritative.score * 100) +
									"%  authoritative",
								parseInt(json.results.emotional.score * 100) + "%  emotional",
								parseInt(json.results.exaggerating.score * 100) + "%  exaggerating"
							];
						})
						.catch(() => {});
				} else {
					this.sentiment = ["Unknown"];
				}
			}
		});
	},
	data: () => {
		return {
			data: {
				data: {}
			},
			typing: false,
			reply: "",
			speaking: false,
			messages: [],
			imageUrl: "",
			undecided: true,
			voice: null,
			sentiment: ["Loading..."],
			options: [
				"Hi Anand, sorry for keeping you waiting",
				"Can you tell me your account number?",
				"Insurance amount of €324 has been transferred via Optiopay"
			],
			nextMessages: [],
			currentQ: null,
			conversationVisible: false,
			joinConversation: false
		};
	},
	methods: {
		approve() {
			const formData = new FormData();
			formData.append("amount", "324");
			fetch("https://myapp-thankful-chimpanzee.cfapps.eu10.hana.ondemand.com/optiopay", {
				body: formData,
				method: "POST"
			})
				.then(response => response.json())
				.then(json => {
					this.messages.push({
						sender: "sender-1",
						attachment: json,
						text: "Confirmation for your new payment",
						avatar: "/bot.svg",
						previous: "sender-3"
					});
					this.saveMessages();
				})
				.catch(() => {});
			console.log("A");
			this.smartSend("I've approved your request");
		},
		decline() {
			this.smartSend("I'm sorry, but I've declined your request");
		},
		smartSend(text, index) {
			if (
				[
					"Can you tell me your account number?",
					"I've approved your request",
					"I'm sorry, but I've declined your request"
				].includes(text)
			) {
				this.messages.push({
					sender: "sender-3",
					text: text,
					avatar: "/manager.jpg",
					botShould: true,
					previous:
						this.messages.length > 0
							? this.messages[this.messages.length - 1].sender
							: "unknown"
				});
				// if (index) {
				// 	this.options = this.options.splice(index, 1);
				// }
				this.saveMessages();
			} else {
				this.sendMessage(text);
			}
		},
		startTalking() {
			if (!this.joinConversation) {
				this.messages.push({
					previous: "sender-1",
					sender: "meta",
					text: "Isabella has joined the conversation"
				});
				this.saveMessages();
			}
			this.conversationVisible = true;
			this.joinConversation = true;
		},
		saveMessages() {
			database.ref(`/${localStorage.sessionID}/conversation`).set(this.messages);
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
				avatar: "/manager.jpg",
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
	overflow: hidden;
	img {
		margin: -1rem;
		width: calc(100% + 2rem);
		max-width: calc(100% + 2rem);
		margin-bottom: 1rem;
	}
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
		font-size: 125%;
		padding: 0 0.75rem;
		display: flex;
		flex-direction: column;
		justify-content: center;
		color: #fff;
	}
	&:nth-of-type(1) .card-icon {
		background-color: #16a085;
	}
	&:nth-of-type(2) .card-icon {
		background-color: #3498db;
	}
	&:nth-of-type(3) .card-icon {
		background-color: #27ae60;
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
	&:nth-of-type(1) {
		background-color: #666;
	}
	&:nth-of-type(2) {
		background-color: #3498db;
	}
}
.yes-no {
	display: flex;
	justify-content: space-between;
	button {
		width: 48%;
	}
	button:nth-child(2) {
		background-color: #27ae60;
		margin-top: 0;
	}
	button:nth-child(1) {
		background-color: #e74c3c;
	}
}
.inline-image {
	overflow: hidden;
	img {
		margin: -1rem;
		width: calc(100% + 2rem);
		max-width: calc(100% + 2rem);
	}
}
</style>
