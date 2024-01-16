const FIRSTNAMES = [
	'John', 'Steve', 'Marc', 'Franklin', 'Isaac', 'Vincent', 'Edwin',
	'Ashlyn', 'Anthony', 'Alia', 'Abby', 'Francesca'
];

const LASTNAMES = [
	'Shafer', 'Whitetaker', 'Glenn', 'Stephens', 'Sherman', 'Howard',
	'Kent', 'Clay', 'Beck', 'Simmons', 'Briggs', 'Lee', 'Maxwell'
];

const TITLES = [
	'CEO', 'President', 'Vice President', 'Director', 'Manager',
	'Developer'
];

const BTN_WIDTH = 4;

document.addEventListener('DOMContentLoaded', () => {
	initCopies();
	initAutoLimits();
	initAutoIncrements();
	initAutoFirstnames();
	initAutoLastnames();
	initAutoTitles();
	initAutoIntegers();
	initPaginations();
});

function initCopies()
{
	let targets = [...document.querySelectorAll('*[data-copy]')];

	targets.reverse().forEach((original) => {
		let amount = parseInt(original.getAttribute('data-copy'));

		for (let i = 0; i < amount; i++) {
			let copy = original.cloneNode(true);

			original.parentNode.insertBefore(copy, original.nextSibling);
		}
	});
}

function initAutoIncrements()
{
	let autos = document.querySelectorAll('.auto-increment');
	
	autos.forEach((auto, i) => {
		auto.innerHTML = i + 1;
	});
}

const rand = (a, b) => Math.floor((Math.random() * b) + a);

function initAutoFirstnames()
{
	let autos = document.querySelectorAll('.auto-firstname');
	
	autos.forEach((auto) => {
		auto.innerHTML = FIRSTNAMES[rand(0, FIRSTNAMES.length)];
	});
}

function initAutoLastnames()
{
	let autos = document.querySelectorAll('.auto-lastname');
	
	autos.forEach((auto) => {
		auto.innerHTML = LASTNAMES[rand(0, LASTNAMES.length)];
	});
}

function initAutoTitles()
{
	let autos = document.querySelectorAll('.auto-title');
	
	autos.forEach((auto) => {
		auto.innerHTML = TITLES[rand(0, TITLES.length)];
	});
}

function initAutoIntegers()
{
	let autos = document.querySelectorAll('.auto-integer');
	
	autos.forEach((auto) => {
		let min = parseInt(auto.getAttribute('min'));
		let max = parseInt(auto.getAttribute('max'));
		
		auto.innerHTML = rand(min, max);
	});
}

function initPaginations()
{
	let paginations = document.querySelectorAll('.pagination');
	
	paginations.forEach((pagination) => {
		let table = document.getElementById(pagination.getAttribute('data-table'));
		
		pagination.setAttribute('data-x', '0');

		if (table !== null && table !== undefined) {
			createPagination(pagination, table);
			
			pagination.closest('.table-container').addEventListener('wheel', (event) => {
				event.preventDefault();

				scrollPages(
					event.wheelDelta
						? event.wheelDelta > 0
						: event.deltaY < 0, pagination,
					table
				);
			});
		}
	});
}

function createPagination(pagination, table)
{
	let limit = parseInt(table.getAttribute("data-limit"));
	let rows = table.querySelectorAll('.table-row:not(.table-heading)');
	let page_count = Math.ceil(rows.length / limit);

	if (isNaN(limit))
		limit = 10;

	rows.forEach((row, index) => {
		if (index >= limit)
			row.style.display = 'none';
	});
	
	for (let i = 0; i < page_count; i++) {
		let new_button = document.createElement('li');

		new_button.innerHTML = "<span>" + (i + 1) + "</span>";
		
		if (i === 0)
			new_button.classList.add('active');

		pagination.appendChild(new_button);
		
		new_button.addEventListener('click', () => {
			switchPage(pagination, table, i);
		});
	}

	updatePaginationInfos(pagination, table, page_count, 0);
	initPaginationExtremes(pagination, table, page_count);
}

function scrollPages(direction, pagination, table)
{
	let last_active = pagination.querySelector('li.active');
	let buttons = pagination.querySelectorAll('li');
	let last_index = Array.from(buttons).indexOf(last_active);
	let scroll_index = null;
	
	if (direction && last_index > 0) {
		scroll_index = last_index - 1;
	} else if (!direction && last_index < buttons.length - 1) {
		scroll_index = last_index + 1;
	}

	if (scroll_index !== null)
		switchPage(pagination, table, scroll_index);
}

function switchPage(pagination, table, index, bypass = -1)
{
	let limit = parseInt(table.getAttribute("data-limit"));
	let rows = table.querySelectorAll('.table-row:not(.table-heading)');
	let buttons = pagination.querySelectorAll('li');
	let last_active = pagination.querySelector('li.active');
	let x_pos = parseInt(pagination.getAttribute('data-x'));
	let x_shift = 0;
	let target_pos = (-index + 2) * BTN_WIDTH;
	let page_count = Math.ceil(rows.length / limit);

	if (bypass !== -1) {
		x_shift = (-bypass + 2) * BTN_WIDTH;
	} else {
		if (index > 1 && index < buttons.length - 2) {
			x_shift = target_pos;
		} else if (index === 1) {
			x_shift = 0;
		} else if (index === page_count - 2) {
			x_shift = (-page_count + 5) * BTN_WIDTH;
		} else {
			x_shift = x_pos;
		}
	}
	
	rows.forEach((row, row_index) => {
		if (row_index < index * limit || row_index >= (index * limit) + limit) {
			row.style.display = 'none';
		} else {
			row.style.display = 'flex';
			row.style.opacity = '0';
			
			setTimeout(() => {
				row.style.opacity = '1';
			}, 50);
		}
	});

	last_active.classList.remove('active');
	buttons[index].classList.add('active');
	pagination.style.transform = 'translateX(' + x_shift + 'rem)';
	pagination.setAttribute('data-x', x_shift);

	updatePaginationInfos(pagination, table, page_count, index);
	updatePaginationProgress(pagination, index, page_count - 1);
}

function updatePaginationInfos(pagination, table, page_count, index)
{
	let info = pagination.closest('.pagination-container').querySelector('.pagination-info');
	
	if (info === null || info === undefined)
		return;

	let from = 0, to = 0;
	let rows = table.querySelectorAll('.table-row:not(.table-heading)');
	let started = false;
	
	for (let i = 1; i < rows.length; i++) {
		let display = rows[i - 1].style.display;
		
		if (display !== 'none' && !started) {
			started = true;
			from = i;
		} else if ((display === 'none' && started) || i == rows.length - 1) {
			to = i == rows.length - 1 ? rows.length : i - 1;
			break;
		}
	}
	
	info.innerHTML = 'Displaying ' + from + '-' + to + ' on page ' + (index + 1) + '/' + page_count;
}

function initPaginationExtremes(pagination, table, max)
{
	let container = pagination.closest('.pagination-container');
	let left = container.querySelector('.pagination-left');
	let right = container.querySelector('.pagination-right');

	if (left !== null && left !== undefined) {
		left.addEventListener('click', () => {
			switchPage(pagination, table, 0, Math.min(2, max - 1));
		});
	}

	if (right !== null && right !== undefined) {
		right.addEventListener('click', () => {
			switchPage(pagination, table, max - 1, Math.max(0, max - 3));
		});
	}

	initPaginationSteppedExtremes(pagination, table, container, max);
}

function initPaginationSteppedExtremes(pagination, table, container, max)
{
	let left = container.querySelector('.pagination-left-one');
	let right = container.querySelector('.pagination-right-one');
	
	if (left !== null && left !== undefined) {
		left.addEventListener('click', () => {
			let last_active = pagination.querySelector('li.active');
			let buttons = pagination.querySelectorAll('li');
			let last_index = Array.from(buttons).indexOf(last_active);
			
			if (last_index > 0)
				switchPage(pagination, table, last_index - 1);
		});
	}
	
	if (right !== null && right !== undefined) {
		right.addEventListener('click', () => {
			let last_active = pagination.querySelector('li.active');
			let buttons = pagination.querySelectorAll('li');
			let last_index = Array.from(buttons).indexOf(last_active);
			
			if (last_index < max - 1)
				switchPage(pagination, table, last_index + 1);
		});
	}
}

function updatePaginationProgress(pagination, index, total)
{
	let dot = pagination.closest('.table-container').querySelector('.progress-point');
	
	dot.style.left = ((index / total) * 100) + '%';
}

function initAutoLimits()
{
	let table_containers = document.querySelectorAll('.table-container');
	let limit = window.innerHeight / 70;
	
	table_containers.forEach((container) => {
		let table = container.querySelector('.table');

		container.setAttribute('style', '--data-limit: ' + limit);
		table.setAttribute('data-limit', limit);
	});
}