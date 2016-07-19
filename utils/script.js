function adjustScroll() {
	//Get scroll position and increment it to adjust with the header size
	var doc = document.documentElement;
	var left = (window.pageXOffset || doc.scrollLeft) - (doc.clientLeft || 0);
	var top = (window.pageYOffset || doc.scrollTop)  - (doc.clientTop || 0);
	window.scrollTo(left, top-45);
}

function jumpEnter(event, total) {
	if (event.which == 13 || event.keyCode == 13) {
		var h = document.getElementById('ref').value;
		if (h > total) {
			h = "bottom";
		} else if (!(h > 1)) {
			h = "top";
		}
		var url = location.href;
		location.href = "#" + h;
		history.replaceState(null, null, url);

		if (h != "bottom") {
			adjustScroll();
		}
	}
}

function jumpButton(total) {
	var h = document.getElementById('ref').value;
	if (h > total) {
		h = "bottom";
	} else if (!(h > 1)) {
		h = "top";
	}
	var url = location.href;
	location.href = "#" + h;
	history.replaceState(null, null, url);

	if (h != "bottom") {
		adjustScroll();
	}
}

function startTime() {
	var today = new Date();
	var weekday = new Array(7);
	weekday[0]=  "Sun";
	weekday[1] = "Mon";
	weekday[2] = "Tue";
	weekday[3] = "Wed";
	weekday[4] = "Thu";
	weekday[5] = "Fri";
	weekday[6] = "Sat";

	var d = weekday[today.getDay()]; 
	var h = today.getHours();
	var m = today.getMinutes();
	m = checkTime(m);
	document.getElementById('txt').innerHTML = d + " " + h + ":" + m;
	var t = setTimeout(startTime, 500);
}

function checkTime(i) {
	if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
	return i;
}

function toggleFullscreen(elem) {
	elem = elem || document.documentElement;
	if (!document.fullscreenElement && !document.mozFullScreenElement && !document.webkitFullscreenElement && !document.msFullscreenElement) {
		if (elem.requestFullscreen) {
			elem.requestFullscreen();
		} else if (elem.msRequestFullscreen) {
			elem.msRequestFullscreen();
		} else if (elem.mozRequestFullScreen) {
			elem.mozRequestFullScreen();
		} else if (elem.webkitRequestFullscreen) {
			elem.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
		}
	} else {
		if (document.exitFullscreen) {
			document.exitFullscreen();
		} else if (document.msExitFullscreen) {
			document.msExitFullscreen();
		} else if (document.mozCancelFullScreen) {
			document.mozCancelFullScreen();
		} else if (document.webkitExitFullscreen) {
			document.webkitExitFullscreen();
		}
	}
}

function adjustImgs() {
	var images = document.getElementById("manga").getElementsByTagName("img");
	for (var i = 0; i < images.length; i++) {
		images[i].style.width = 850;
	}
}

function incImgsSize() {
	var tmp = window.pageYOffset/document.body.scrollHeight;

	var images = document.getElementById("manga").getElementsByTagName("img");
	for (var i = 0; i < images.length; i++) {
		var width = parseInt(images[i].style.width.replace("px", ""));
		if (width >= 1650) {
			break;
		}
		images[i].style.width = width + 50;
	}

	window.scrollTo(0, document.body.scrollHeight*tmp);
}

function decImgsSize() {
	var tmp = window.pageYOffset/document.body.scrollHeight;

	var images = document.getElementById("manga").getElementsByTagName("img");
	for (var i = 0; i < images.length; i++) {
		var width = parseInt(images[i].style.width.replace("px", ""));
		if (width <= 550) {
			break;
		}
		images[i].style.width = width - 50;
	}

	window.scrollTo(0, document.body.scrollHeight*tmp);
}
