<template>
	<section>
		<!-- <header class="title">Ava</header> -->
		<main class="main-chat">
			<div v-for="(message, index) in messages" :key="`message${index}`" v-bind:class="`message-block ${message.sender} next-${message.next || 'none'} previous-${message.previous || 'none'} class-${message.class || 'none'}`">
				<div v-if="message.sender === `meta`" class="message-meta">
					<div class="details">{{message.text}}</div>
				</div>
				<div v-else-if="message.sender === `sender-1`" class="message-content">
					<div class="sender">
						<img alt="Sender's Avatar" :src="message.avatar">
					</div>
					<div class="message">{{message.text}}</div>
				</div>
				<div v-else class="message-content">
					<div class="message">{{message.text}}</div>
					<div class="sender">
						<img alt="Sender's Avatar" :src="message.avatar">
					</div>
				</div>
			</div>
			<div class="message-block sender-1 typing" v-if="typing">
				<div class="message-content">
					<div class="sender">
						<img alt="Sender's Avatar" :src="currentImage">
						</div>
					<div class="message">
						<span class="ellipsis-1">&bullet;</span>
						<span class="ellipsis-2">&bullet;</span>
						<span class="ellipsis-3">&bullet;</span>
					</div>
				</div>
			</div>
		</main>
		<footer>
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
import FontAwesomeIcon from "@fortawesome/vue-fontawesome";
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
		this.messages = this.$store.state.messages;
		if (this.messages.length === 0) {
			this.botSays(`Hi 👋`);
			this.botSays(`I'm Ava from Talanx`);
			this.botSays(`How can I help?`, ["Insurance claim", "Help"]);
		} else {
			this.options = this.messages[this.messages.length - 1].options;
		}
	},
	data: () => {
		return {
			currentImage: "/bot.svg",
			typing: false,
			reply: "",
			speaking: false,
			messages: [],
			voice: null,
			options: []
		};
	},
	methods: {
		animateButton(text) {
			if (!this.messages) return;
			console.log("Your selected", text);
			let animator = document.createElement("div");
			animator.innerHTML = text;
			animator.classList.add("animator");
			document.body.appendChild(animator);
			this.messages.push({
				sender: "sender-2",
				text: text,
				class: "temp",
				avatar: "/sender.png",
				previous:
					this.messages.length > 0
						? this.messages[this.messages.length - 1].sender
						: "unknown"
			});
			setTimeout(() => {
				const elements = document.querySelectorAll(".options li button");
				document.querySelector(".options ul").style.opacity = "0";
				document.querySelector(".options ul").addEventListener("transitionend", () => {
					document.querySelector(".options ul").style.display = "none";
				});
				elements.forEach(element => {
					if (element.innerText === text) {
						element.style.visibility = "hidden";
						const bound = getOffset(element);
						animator.style.width = `${element.offsetWidth + 1}px`;
						animator.style.top = `${bound.top}px`;
						animator.style.opacity = "1";
						animator.style.left = `${bound.left}px`;
					}
				});
			}, 1);
			setTimeout(() => {
				const element = document.querySelector(".class-temp .message");
				element.parentNode.querySelector(".class-temp .sender img").style.opacity = "1";
				const bound = getOffset(element);
				animator.style.transition = `1s`;
				animator.style.top = `${bound.top - this.$el.querySelector("main").scrollTop}px`;
				animator.style.left = `${bound.left}px`;
				animator.addEventListener("transitionend", () => {
					try {
						animator.parentNode.removeChild(animator);
						this.messages.pop();
						this.sendMessage(text);
					} catch (e) {}
					return;
				});
			}, 10);
		},
		startSpeech() {
			if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
				this.speaking = true;
				const recognition = new webkitSpeechRecognition() || new SpeechRecognition();
				recognition.start();
				recognition.addEventListener("result", text => {
					recognition.stop();
					this.sendMessage(text.results[0][0].transcript);
					this.speaking = false;
				});
			}
		},
		respond(text) {
			this.options = [];
			let currentTime = new Date().getTime();
			return new Promise((resolve, reject) => {
				setTimeout(() => {
					this.typing = true;
				}, 200);
				let result = "Hello, world";
				setTimeout(() => {
					this.typing = false;
					resolve({
						text: result,
						options: [`Option ${Math.random()}`, `Option ${Math.random()}`]
					});
				}, new Date().getTime() - currentTime > 1000 ? 0 : 1000 - (new Date().getTime() - currentTime));
			});
		},
		botSays(text, options = []) {
			if (this.messages.length > 0) {
				this.messages[this.messages.length - 1].next = "sender-1";
			}
			if ("speechSynthesis" in window) {
				let voices = window.speechSynthesis.getVoices();
				const utterThis = new SpeechSynthesisUtterance(
					text.replace(
						/([\uE000-\uF8FF]|\uD83C[\uDF00-\uDFFF]|\uD83D[\uDC00-\uDDFF])/g,
						""
					)
				);
				let a = setInterval(() => {
					voices = window.speechSynthesis.getVoices();
					voices.forEach(voice => {
						if (voice.name === "Google US English") {
							utterThis.voice = voice;
						}
					});
					if (voices.length > 0) {
						clearInterval(a);
						window.speechSynthesis.speak(utterThis);
					}
				}, 10);
				setTimeout(() => {
					clearInterval(a);
				}, 2000);
			}
			const message = {
				sender: "sender-1",
				text: text,
				avatar: this.currentImage,
				previous:
					this.messages.length > 0
						? this.messages[this.messages.length - 1].sender
						: "unknown"
			};
			if (options) {
				message.options = options;
				this.options = options;
			}
			this.messages.push(message);
			this.$store.commit("update", this.messages);
		},
		sendMessage(reply = this.reply) {
			if (typeof reply !== "string") reply = this.reply;
			this.reply = "";
			if (!reply || !reply.trim()) return;
			if (reply.toLowerCase() === "clear") {
				this.messages = [];
				this.$store.commit("update", this.messages);
				location.reload();
				return;
			}
			if (this.messages.length > 0) {
				this.messages[this.messages.length - 1].next = "sender-2";
			}
			this.messages.push({
				sender: "sender-2",
				text: reply,
				avatar: "/sender.png",
				previous:
					this.messages.length > 0
						? this.messages[this.messages.length - 1].sender
						: "unknown"
			});
			this.$store.commit("update", this.messages);
			setTimeout(() => {
				this.$el.querySelector("main").scrollTop = this.$el.querySelector(
					"main"
				).scrollHeight;
			}, 1);
			this.respond()
				.then(response => {
					this.botSays(response.text, response.options);
					setTimeout(() => {
						this.$el.querySelector("main").scrollTop = this.$el.querySelector(
							"main"
						).scrollHeight;
					}, 1);
				})
				.catch(() => {});
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
			color: #cb0056;
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
		transition: 1s;
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
				background-color: #cb0056;
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
		transition: 1s;
	}
}
input {
	outline: none;
}
</style>
