<template>
	<section>
		<header class="title" style="padding: 0.5rem 0">
			<img alt="HDI" src="/hdilogo.png" style="height: 35px">
		</header>
		<main class="main-chat">
			<div v-for="(message, index) in messages" :key="`message${index}`" v-bind:class="`message-block ${message.sender} next-${message.next || 'none'} previous-${message.previous || 'none'} class-${message.class || 'none'}`">
				<div v-if="message.sender === `meta`" class="message-meta">
					<div class="details">{{message.text}}</div>
				</div>
				<div v-else-if="message.sender === `sender-2`" class="message-content">
					<div class="message">
						<div class="message-inner" v-if="!message.text.includes(`IMAGE_URL|`)">{{message.text}}</div>
						<div class="message-inner inline-image" v-else>
							<div v-if="imageUrl"><img alt="Uploaded image" :src="imageUrl"></div>
							<div v-else><font-awesome-icon icon="sync" spin /> &nbsp;Loading...</div>
						</div>
					</div>
					<div class="sender">
						<img alt="Sender's Avatar" :src="message.avatar">
					</div>
				</div>
				<div v-else class="message-content">
					<div class="sender">
						<img alt="Sender's Avatar" :src="message.avatar">
					</div>
					<div class="message">
						<div class="message-inner">{{message.text}}</div>
						<div class="has-attachment" v-if="message.attachment">
							<div>{{message.attachment.accessCode}}</div>
							<div>{{message.attachment.amount.currency}} {{message.attachment.amount.amount}}</div>
							<div><strong>BIC</strong> {{message.attachment.fallbackBankAccount.bic}}</div>
							<div><strong>IBAN</strong> {{message.attachment.fallbackBankAccount.iban}}</div>
						</div>
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
					<input type="text" v-model="reply" @keyup="textChanged" placeholder="Enter a message...">
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
import chrono from "chrono-node";
import sentenceCase from "sentence-case";
import FontAwesomeIcon from "@fortawesome/vue-fontawesome";
import replies from "../../modules/replies";
firebase.initializeApp({
	apiKey: "AIzaSyDZGcrdh48alSZlUoiQSpXP0fktcVPJf2w",
	authDomain: "talanx-hack.firebaseapp.com",
	databaseURL: "https://talanx-hack.firebaseio.com",
	projectId: "talanx-hack",
	storageBucket: "talanx-hack.appspot.com",
	messagingSenderId: "784808067653"
});
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
		if (localStorage.sessionID) {
			const messages = firebase.database().ref(`/${localStorage.sessionID}/conversation`);
			messages.once("value").then(snapshot => {
				this.messages = snapshot.val() || [];
				if ((snapshot.val() || []).length === 0) {
					this.botSays(`Hi 👋`);
					setTimeout(() => {
						this.botSays(`I'm Ava from Talanx`);
					}, 200);
					setTimeout(() => {
						this.botSays(`How can I help?`, ["Insurance claim", "Introduction"]);
					}, 400);
				} else {
					this.options = snapshot.val()[snapshot.val().length - 1].options || [];
				}
				setTimeout(() => {
					this.$el.querySelector("main").scrollTop = this.$el.querySelector(
						"main"
					).scrollHeight;
				}, 1);
			});
			messages.on("value", snapshot => {
				if (snapshot.val() && (snapshot.val() || []).length > 0) {
					if (!!snapshot.val()[snapshot.val().length - 1].botShould) {
						console.log("botShould");
						this.respond(snapshot.val()[snapshot.val().length - 1].text)
							.then(response => {
								this.respondResponse(response);
							})
							.catch(() => {});
					}
					this.messages = snapshot.val() || [];
					setTimeout(() => {
						this.$el.querySelector("main").scrollTop = this.$el.querySelector(
							"main"
						).scrollHeight;
					}, 1);
					this.messages.forEach(message => {
						if (message.text === "Isabella has joined the conversation") {
							this.bossHasJoined = true;
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
					});
				}
			});
		} else {
			localStorage.sessionID = Math.random()
				.toString(36)
				.slice(2);
			fetch(
				"https://myapp-thankful-chimpanzee.cfapps.eu10.hana.ondemand.com/force-refresh-chat"
			)
				.then(() => {
					fetch(
						"https://myapp-thankful-chimpanzee.cfapps.eu10.hana.ondemand.com/begin-session "
					)
						.then(() => {})
						.catch(() => {})
						.finally(() => {
							this.sendMessage("clear");
						});
				})
				.catch(() => {});
		}
	},
	data: () => {
		return {
			currentImage: "/bot.svg",
			typing: false,
			imageUrl: "",
			reply: "",
			speaking: false,
			messages: [],
			voice: null,
			options: [],
			nextMessages: [],
			currentQ: null,
			bossHasJoined: false
		};
	},
	methods: {
		textChanged() {
			if (this.currentQ === "place_name" && this.reply.trim().length > 0) {
				fetch(
					`https://myapp-thankful-chimpanzee.cfapps.eu10.hana.ondemand.com/map-autocomplete?text=${encodeURIComponent(
						this.reply
					)}`
				)
					.then(response => response.json())
					.then(json => {
						this.options = [];
						json.predictions.forEach(place => {
							this.options.push(place.description);
						});
					})
					.catch(() => {});
			}
		},
		saveMessages() {
			database.ref(`/${localStorage.sessionID}/conversation`).set(this.messages);
		},
		animateButton(text) {
			if (!this.messages) return;
			if (text === "Click photo") {
				const fileUploader = document.createElement("input");
				fileUploader.setAttribute("type", "file");
				fileUploader.style.display = "none";
				document.body.appendChild(fileUploader);
				fileUploader.click();
				fileUploader.addEventListener("change", () => {
					const storageRef = firebase.storage().ref();
					const url = `upload/${Math.random()
						.toString(36)
						.slice(2)}.jpg`;
					const ref = storageRef.child(url);
					this.options[0] = "Uploading image...";
					ref.put(fileUploader.files[0]).then(snapshot => {
						database.ref(`/${localStorage.sessionID}/conversation`).update({
							imageUrl: url
						});
						this.currentQ = "image_upload";
						setTimeout(() => {
							fileUploader.parentNode.removeChild(fileUploader);
							this.sendMessage(`IMAGE_URL|${url}`);
						}, 10);
					});
				});
				return;
			}
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
				animator.style.transition = `300ms`;
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
					this.sendMessage(sentenceCase(text.results[0][0].transcript));
					this.speaking = false;
				});
			}
		},
		respond(text) {
			this.options = [];
			let currentTime = new Date().getTime();
			return new Promise((resolve, reject) => {
				this.typing = true;
				if (this.currentQ !== null) {
					switch (this.currentQ) {
						case "image_upload":
							resolve({
								text: "Thanks, that's all I need 👌"
							});
							this.nextMessages = [
								{
									text: "I'm inviting my colleague to approve your request"
								}
							];
							this.currentQ = null;
							break;
						case "place_name":
							resolve({
								text: "Click a photo to verify your claim",
								options: ["Click photo"]
							});
							this.currentQ = "image_upload";
							break;
						case "when_happened":
							resolve({
								text: "Okay, any idea where it happened?"
							});
							this.currentQ = "place_name";
							break;
						case "covered_in_insurance":
							if (text.toLowerCase().includes("yes")) {
								resolve({
									text: "When did this incident happen?",
									options: ["Today", "Yesterday", "April 28"]
								});
								this.currentQ = "when_happened";
							} else {
								resolve({
									text:
										"Okay, let me know if there's anything else I can do for you 😊"
								});
								this.currentQ = null;
							}
							break;
						case "insurance_claim":
							this.nextMessages = [
								{
									text: "Could you tell me more about the incident?"
								}
							];
							resolve({
								text: `${
									this.messages[this.messages.length - 1].text
								} insurance, sounds good`
							});
							this.currentQ = null;
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
						.then(response => {
							if (response.ok) {
								return response.json();
							} else {
								fetch(
									"https://myapp-thankful-chimpanzee.cfapps.eu10.hana.ondemand.com/force-refresh-chat"
								)
									.then(() => {
										fetch(
											"https://myapp-thankful-chimpanzee.cfapps.eu10.hana.ondemand.com/begin-session "
										)
											.then(() => {})
											.catch(() => {})
											.finally(() => {
												this.sendMessage("clear");
											});
									})
									.catch(() => {});
							}
						})
						.then(json => {
							let result = "unknown";
							const answers = json.answers;
							const answer = answers[answers.length - 1];
							if (answer.attributes.ANSWER_TEXT) {
								result = answer.attributes.ANSWER_TEXT;
								if (["insurance_claim", "covered_in_insurance"].includes(result)) {
									this.currentQ = result;
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
								text: "🙂"
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
				utterThis.rate = 1.25;
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
			this.saveMessages();
		},
		sendMessage(reply = this.reply) {
			if (typeof reply !== "string") reply = this.reply;
			this.reply = "";
			if (!reply || !reply.trim()) return;
			if (reply.toLowerCase() === "clear") {
				this.messages = [];
				this.saveMessages();
				database.ref(`/${localStorage.sessionID}/data`).set({});
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
			this.saveMessages();
			setTimeout(() => {
				this.$el.querySelector("main").scrollTop = this.$el.querySelector(
					"main"
				).scrollHeight;
			}, 1);
			if (this.currentQ) {
				const updator = {};
				if (this.currentQ === "when_happened") {
					updator[this.currentQ] = chrono.parseDate(reply);
				} else {
					updator[this.currentQ] = reply;
				}
				database.ref(`/${localStorage.sessionID}/data`).update(updator);
			}
			if (!this.bossHasJoined) {
				this.respond(reply)
					.then(response => {
						this.respondResponse(response);
					})
					.catch(() => {});
			}
		},
		respondResponse(response) {
			this.botSays(response.text, response.options);
			setTimeout(() => {
				this.$el.querySelector("main").scrollTop = this.$el.querySelector(
					"main"
				).scrollHeight;
			}, 1);
			let l = this.nextMessages.length;
			let count = 0;
			let x = setInterval(() => {
				this.typing = false;
				if (count === l) {
					this.nextMessages = [];
					clearInterval(x);
					return;
				}
				this.botSays(this.nextMessages[count].text, this.nextMessages[count].options);
				setTimeout(() => {
					this.$el.querySelector("main").scrollTop = this.$el.querySelector(
						"main"
					).scrollHeight;
				}, 1);
				count++;
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
			background-color: #16a085;
			color: #fff;
		}
	}
	&.sender-1 + .sender-2,
	&.sender-1 + .sender-3,
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
	&.sender-2.next-sender-2 {
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
	&.sender-2.next-sender-2.previous-sender-2 {
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
			color: #16a085;
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
				background-color: #16a085;
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
.inline-image {
	overflow: hidden;
	img {
		margin: -1rem;
		width: calc(100% + 2rem);
		max-width: calc(100% + 2rem);
	}
}
.has-attachment {
	background-color: #34495e;
	color: rgba(255, 255, 255, 0.75);
	padding: 1rem;
	margin: 0.25rem 0;
	border-radius: 15px;
	:first-child {
		text-align: center;
		color: #fff;
	}
}
</style>
