let profilButton = document.getElementById('profil');
let profilPreview = document.getElementById('profil-preview');


profilButton.addEventListener('click', function () {
    profilPreview.classList.toggle('active');
});




let sidebar = document.querySelector('.sidebar-icons');
let right = document.getElementById('content');
let subsidebar = document.querySelector('.subsidebar');

sidebar.addEventListener('mouseover', function() {
    right.classList.add('active');
    subsidebar.classList.add('active');
});

sidebar.addEventListener('mouseout', function() {
    right.classList.remove('active');
    subsidebar.classList.remove('active');
});

subsidebar.addEventListener('mouseover', function() {
    right.classList.add('active');
    subsidebar.classList.add('active');
});

subsidebar.addEventListener('mouseout', function() {
    right.classList.remove('active');
    subsidebar.classList.remove('active');
});



let elements_withsub = document.querySelectorAll('.with-sub');
let sub_elements = document.querySelectorAll('.dropdown-content');

elements_withsub.forEach(function(item) {
    item.addEventListener('mouseover', function() {
        item.children[1].classList.add('active');
    });
    
    item.addEventListener('mouseout', function() {
        item.children[1].classList.remove('active');
    });
});

sub_elements.forEach(function(item) {
    item.addEventListener('mouseover', function() {
        item.classList.add('active');
    });

    item.addEventListener('mouseout', function() {
        item.classList.remove('active');
    });
});
