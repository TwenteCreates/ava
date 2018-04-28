<template>
	<nav class="navbar">
		<ul>
			<li>
				<router-link to="/menu">
					<div><font-awesome-icon icon="bars" /></div>
					<div>Menu</div>
				</router-link>
			</li>
			<li>
				<router-link to="/">
					<div><font-awesome-icon icon="comment" /></div>
					<div>Ava</div>
				</router-link>
			</li>
			<li>
				<router-link to="/profile">
					<div><font-awesome-icon icon="cog" /></div>
					<div>Settings</div>
				</router-link>
			</li>
		</ul>
	</nav>
</template>

<script>
import FontAwesomeIcon from "@fortawesome/vue-fontawesome";
export default {
	components: {
		FontAwesomeIcon
	}
};
</script>


<style lang="scss" scoped>
.navbar {
	background-color: #fff;
	box-shadow: 0 -0.5rem 1rem rgba(0, 100, 100, 0.1);
	z-index: 999;
	ul {
		margin: 0;
		padding: 0;
		display: flex;
		li {
			width: 100%;
			text-align: center;
			a {
				color: inherit;
				font-size: 80%;
				display: block;
				padding: 0.5rem 0 0.25rem 0;
				opacity: 0.75;
				text-decoration: none;
				svg {
					font-size: 150%;
				}
				&.router-link-exact-active {
					color: #cb0056;
					opacity: 1;
				}
			}
		}
	}
}
</style>
