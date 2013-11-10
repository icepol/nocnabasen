var pridaj_vers_top;

$(window).load(function(){
	$('#main').masonry({
		itemSelector: '.box',
		columnWidth: 300,
		isAnimated: true
	});
});

$('document').ready(function(){
	if ($("#pridaj-vers").size()) {
		// scrollovanie formu v nocnej basni
		pridaj_vers_top = $("#pridaj-vers").offset().top;
		$("#pridaj-vers").css("top", pridaj_vers_top);
		
		pridaj_vers_height = $("#pridaj-vers").height();
		
		window.onscroll = document.documentElement.onscroll = set_offset;
		
		if ($.cookie("scroll")) {
			if (document.documentElement.scrollTop)
				document.documentElement.scrollTop = $(document).height();
			else
				document.body.scrollTop = $(document).height();
		}
		else {
			$.cookie("scroll", "1", { expires: 365 });
		}
	}
	
	if ($("#pridaj-text").size()) {
		// ak su zobrazene blogy
		$(".type").click(function(){
			// zmena typu pridavaneho contentu
			var form_name = '#pridaj-' + $(this).attr('href');
			if ($(form_name).css('display') == 'none') {
				$("#pridaj-text").css('display', 'none');
				$("#pridaj-foto").css('display', 'none');
				$(form_name).css('display', 'block');
				
				$(".type").removeClass('active');
				$(this).addClass('active');
			}
			
			return false;
		});
		
		$(".foto").click(function(){
			return show_foto(this);
		});
		
		$("#pridaj-text").submit(function(event){
			// pridanie textoveho prispevku
			if ($("#topic").val() == '' || $("#topic").val().length > 200) {
				$("#topic").addClass('alert');
				return false;
			}
			
			if ($(".category").val() == '') {
				$(".category").addClass('alert');
				return false;
			}
			
			$('.pridat').attr('disabled', 1);
			return true;
		});
		
		$("#pridaj-foto").submit(function(event){
			// pridanie fotky
			if ($(".category").val() == '') {
				$(".category").addClass('alert');
				return false;
			}
			
			if (!$("#author").attr('checked')) {
				$("#author-label").addClass('alert');
				return false;
			}
			
			$('.pridat').attr('disabled', 1);
			return true;
		});
		
		$("#topic").focus(function() {
			return update_counter();
		});
		$("#topic").keypress(function() {
			return update_counter();
		});
		$("#topic").keyup(function() {
			return update_counter();
		});
		
		$("#topic").change(function(){
			if ($(this).hasClass('alert')) {
				$(this).removeClass('alert');
			}
			
			return update_counter();
		});
		
		$("#topic").blur(function() {
			hide_counter();
		});
		
		$(".category").change(function(){
			$(".category").val($(this).val());
			if ($(this).hasClass('alert')) {
				$(this).removeClass('alert');
			}
		});

		if (input_form) {
			var form_name = '#pridaj-' + input_form;
			if ($(form_name).css('display') == 'none') {
				$("#pridaj-text").css('display', 'none');
				$("#pridaj-foto").css('display', 'none');
				$(form_name).css('display', 'block');
				
				$(".type").removeClass('active');
				$('#li-' + input_form).addClass('active');
			}
		}
		
		$('.category-filter').click(function(){
			// filtrovanie contentu podla kategorie
			$.cookie("category_id", $(this).attr('href'), {});
			$('.category-filter').removeClass('active');
			$(this).addClass('active');
			
			// refresh
			location = location;
			
			return false;
		});
	}
		
	$("#comments").css('display', 'none');
	$(".comment").click(function(event) {
		var href = $(this).attr('href');
		$.ajax({
			url: href,
			type: "GET",
			success: function(data) {
				show_comments(data, href);
			}
		});
		
		return false;
	});
	
	if (comments) {
		// ak su poslane aj commenty, tak ich hned zobrazime
		var href = location.href;
		show_comments(comments, href);
	}

	$(".foto").click(function(){
		return show_foto(this);
	});
		
	author_filter();
	
	set_delete_event();
});

function set_delete_event() {
	$('.delete_topic').click(function() {
		if (!confirm('Naozaj zmazať príspevok?')) {
			return false;
		}
		
		return true;
	});
	
	$('.delete_comment').click(function() {
		if (!confirm('Naozaj zmazať komentár?')) {
			return false;
		}
		
		var href = $(this).attr('href') + '?ajax';
		$.ajax({
			url: href,
			type: "POST", 
			success: function(data) {
				show_comments(data, href);
			}
		});
		
		return false;
	});
}

function update_counter() {
	$('#counter').css('display', 'block');
	$('#counter').html('ostáva: ' + (200 - $("#topic").val().length));
	
	if ($("#topic").val().length >= 200) {
		return false;
	}
	else {
		return true;
	}
}

function hide_counter() {
	$('#counter').css('display', 'none');
}

function show_comments(data, href) {
	var top = document.documentElement.scrollTop || document.body.scrollTop;
	var left = ($(window).width() - parseInt($("#comments").css('width'))) / 2;
	
	$("#comments").html(data);
	$("#comments").css('top', top);
	$("#comments").css('left', left);
	
	$(".close").click(function(){
		$("#comments").css('display', 'none');
		return false;
	});
	
	// pridanie commentu
	$("#pridaj-comment").submit(function(event){
		add_comment(event, href);
	});
	
	$("#comments").css('display', 'block');
	
	author_filter();
	
	$(".foto").click(function(){
		return show_foto(this);
	});
	
	$(".add_essay_photo").click(function(){
		return add_essay_photo($(this));
	});
	
	set_delete_event();
}

function author_filter() {
	$('.author-filter').click(function() {
		// filtrovanie contentu podla autora
		$.cookie("author_id", $(this).attr('href'), {});
		
		// refresh
		location = location;
		
		return false;
	});
	
	if ($.cookie("author_id")) {
		$('.author-filter').css('text-decoration', 'line-through');
	}
}

function add_comment(event, href) {
	event.preventDefault();
	
	if ($("#comment").val() == '' || $("#comment").val().length > 200) {
		$("#comment").addClass('alert');
		return false;
	}
	
	$('.pridat').attr('disabled', 1);
	$.ajax({
		url: href,
		type: "POST",
		data: {
            comment: $("#comment").val(),
            csrfmiddlewaretoken: $.cookie('csrftoken')
        },
		success: function(data) {
			$("#comments").html(data);
			
			$(".close").click(function(){
				$("#comments").css('display', 'none');
				return false;
			});
			
			// pridanie commentu
			$("#pridaj-comment").submit(function(event){
				add_comment(event, href);
			});
			
			$('.pridat').attr('disabled', false);
		}
	});
	
	return false;
}

function set_offset() {
	var offset = document.documentElement.scrollTop || document.body.scrollTop;
	var top = parseInt($("#pridaj-vers").css("top"));
	
	var new_top = pridaj_vers_top;
	
	if (offset > 10) {
		new_top = offset + $(window).height() - pridaj_vers_height - 40;
	}
	
	if (new_top != top) {
		$("#pridaj-vers").animate(
			{ top: new_top },
			{ duration: 50}
		);
	}
}

function show_foto(t) {
	// zobrazenie velkej fotografie
	var top = document.documentElement.scrollTop || document.body.scrollTop;
	var left = ($(window).width() - parseInt($("#photo_big").css('width'))) / 2;
	
	var data = '<img src="' + $(t).attr('href') + '" />';
	$("#photo_big .content").html(data);
	$("#photo_big").css('top', top);
	$("#photo_big").css('left', left);
	
	$(".photo_close").click(function(){
		$("#photo_big").css('display', 'none');
		return false;
	});
	
	$("#photo_big").css('display', 'block');
	
	return false;
}

function add_essay_photo(t) {
	var href = t.attr('href') + '/?ajax';
	$.ajax({
		url: site_root + '/add_essay_photo/' + href,
		type: "POST", 
		success: function(data) {
			if (data) {
				// show form
				$('#add_essay_photo').html(data);
				
				$("#essay_photo_form").submit(function(event){
					// pridanie fotky do esseje
					if (!$("#essay_photo_author").attr('checked')) {
						$("#essay_photo_author_label").addClass('alert');
						return false;
					}
					
					$('.pridat').attr('disabled', 1);
					return true;
				});
			}
			else {
				// reload comments
				alert(href);
				$.ajax({
					url: site_root + '/' + href,
					type: "POST", 
					success: function(data) {
						show_comments(data, href);
					}
				});
			}
		}
	});
	
	return false;
}

function home() {
	window.location = '/';
}