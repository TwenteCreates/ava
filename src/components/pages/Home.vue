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
					<div class="message">
						<div class="message-inner">{{message.text}}</div></div>
				</div>
				<div v-else class="message-content">
					<div class="message">
						<div class="message-inner">{{message.text}}</div></div>
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
						<div class="message-inner">
							<span class="ellipsis-1">&bullet;</span>
							<span class="ellipsis-2">&bullet;</span>
							<span class="ellipsis-3">&bullet;</span>
						</div>
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
import replies from "../../modules/replies";
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
		// fetch("https://myapp-thankful-chimpanzee.cfapps.eu10.hana.ondemand.com/force-refresh-chat")
		// 	.then(() => {
		// 		fetch(
		// 			"https://myapp-thankful-chimpanzee.cfapps.eu10.hana.ondemand.com/begin-session "
		// 		)
		// 			.then(() => {})
		// 			.catch(() => {});
		// 	})
		// 	.catch(() => {});
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
			options: [],
			nextMessages: [],
			currentQ: null
		};
	},
	methods: {
		animateButton(text) {
			if (!this.messages) return;
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
				let element = document.querySelector(".class-temp .message-inner");
				element.parentNode.parentNode.querySelector(
					".class-temp .sender img"
				).style.opacity =
					"1";
				const bound = getOffset(element);
				animator.style.transition = `500ms`;
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
				if (this.currentQ !== null) {
					switch (this.currentQ) {
						case "insurance_claim":
							this.currentQ;
							this.nextMessages = [
								{
									text: "Could you tell us more about the incident?"
								}
							];
							resolve({
								text: `${
									this.messages[this.messages.length - 1].text
								} insurance, sounds good`
							});
							break;
						default:
							this.currentQ = null;
							break;
					}
				} else {
					fetch(
						`https://myapp-thankful-chimpanzee.cfapps.eu10.hana.ondemand.com/get-answer?text=${encodeURIComponent(
							text.toLowerCase()
						)}`
					)
						.then(response => response.json())
						.then(json => {
							let result = "unknown";
							const answers = json.answers;
							console.log(answers, answers.length);
							for (let i = 0; i < answers.length; i++) {
								let answer = answers[i];
								console.log(answer);
								if (answer.attributes.ANSWER_TEXT) {
									result = answer.attributes.ANSWER_TEXT;
									console.log("RESULT", result);
									if (result === "insurance_claim") {
										this.currentQ = "insurance_claim";
									}
								}
							}
							if (replies[result]) {
								if (replies[result].length > 1) {
									const texts = replies[result].slice();
									const untexts = replies[result][0];
									texts.shift();
									this.nextMessages = texts;
									resolve(untexts);
								} else {
									resolve(replies[result][0]);
								}
							} else {
								resolve({
									text: "I'm sorry, I don't understand"
								});
							}
							setTimeout(() => {
								this.typing = false;
								resolve({
									text: result,
									options: [`Option ${Math.random()}`, `Option ${Math.random()}`]
								});
							}, new Date().getTime() - currentTime > 1000 ? 0 : 1000 - (new Date().getTime() - currentTime));
						})
						.catch(error => {
							resolve({
								text: "I wasn't able to answer your query"
							});
							this.typing = false;
						});
				}
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
			this.respond(reply)
				.then(response => {
					this.botSays(response.text, response.options);
					setTimeout(() => {
						this.$el.querySelector("main").scrollTop = this.$el.querySelector(
							"main"
						).scrollHeight;
					}, 1);
					let l = this.nextMessages.length;
					let count = 0;
					let x = setInterval(() => {
						if (count === l) {
							this.nextMessages = [];
							clearInterval(x);
							this.typing = false;
							return;
						}
						this.botSays(
							this.nextMessages[count].text,
							this.nextMessages[count].options
						);
						setTimeout(() => {
							this.$el.querySelector("main").scrollTop = this.$el.querySelector(
								"main"
							).scrollHeight;
						}, 1);
						count++;
					}, 1000);
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
	&.sender-2 {
		.message-inner {
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
		.message {
			display: flex;
			justify-content: flex-end;
		}
		.sender {
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
		transition: 500ms;
	}
}
input {
	outline: none;
}
</style>
