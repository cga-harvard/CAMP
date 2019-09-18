window.onload=function(){
	 setImgHeight();//set the height according to the width, the rate is 4:3[noData.jpg]
}
//be activated when browser's size is changed
window.onresize=function(){
	 setImgHeight();//set the height according to the width, the rate is 4:3[noData.jpg]
}
//set the selectchange event of category selectpicker
function selectOnChange1(obj){
	var value = obj.options[obj.selectedIndex].value;
	showMaps("tmi1","hottest",value);
}
function selectOnChange2(obj){
	var value = obj.options[obj.selectedIndex].value;
	showMaps("tmi2","latest", value);
}
function showCategorys(language){
	var url = "/api/categories";
	var data = null;
	var csrftoken = getCookie('csrftoken');
	$.ajax({
		url: url,
		async: false,
		cache: false,
		type: "GET",
		success: function (res) {
			data = $.parseJSON(res);
		},
		beforeSend: function(xhr, settings) {
		  xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	});
	var selectHTML = "";
	for(category in data.objects){
		var categoryid = parseInt(category.id);
		var categorydescription = category.gn_description_zh_cn;
		selectHTML += "<option value="+categoryid+">"+categorydescription+"</option>"
	}
	$("#category1").append(selectHTML);
	$("#category2").append(selectHTML);
    $("#category1").selectpicker('refresh');
    $("#category2").selectpicker('refresh');
}
function showMaps(divIdPrefix, type, category){
	var result = null;
	var url = "/maps/list/hottest/";
	var csrftoken = getCookie('csrftoken');
	$.ajax({
		url: url,
		async: false,
		type: "POST",
		data: {
			category: category,
			type: type
		},
		success: function (res) {
			result = $.parseJSON(res);
		},
		beforeSend: function(xhr, settings) {
		  xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	});
	for(var i = 0; i< 6; i++)
	{
		var mapname, curdiv, imgurl, mapurl, img;
		if(result[i] != null)
		{
			mapname = result[i][0];
			username = result[i][1];
			curdiv = divIdPrefix + (i+1);
			imgurl = result[i][2];
			mapurl = result[i][3];
			popularcount = result[i][4];
			date = result[i][5];
			img = $("#"+curdiv).find("img");
			$("#"+curdiv).attr("onclick","location='"+mapurl+"'");
			$("#"+curdiv).children("p")[0].innerHTML = gettext("Title:") + mapname;

					/* DO WE NEED ALL THIS?
            // if(type=="admin"){
            	if(mapurl.split("/")[2]==26||mapurl.split("/")[2]==41||mapurl.split("/")[2]==45||mapurl.split("/")[2]==46||mapurl.split("/")[2]==48||mapurl.split("/")[2]==52||mapurl.split("/")[2]==54||mapurl.split("/")[2]==59||mapurl.split("/")[2]==71||mapurl.split("/")[2]==78||mapurl.split("/")[2]==82||mapurl.split("/")[2]==97||mapurl.split("/")[2]==99||mapurl.split("/")[2]==102||mapurl.split("/")[2]==107||mapurl.split("/")[2]==117||mapurl.split("/")[2]==118||mapurl.split("/")[2]==120||mapurl.split("/")[2]==122||mapurl.split("/")[2]==124||mapurl.split("/")[2]==129||mapurl.split("/")[2]==132||mapurl.split("/")[2]==135||mapurl.split("/")[2]==139){
					imgurl =window.location.href+"static/img/thumb/map"+mapurl.split("/")[2]+".jpg";
				}
                if (mapname=="李白行迹图") {
                    imgurl =window.location.href+"static/img/slide-libai.gif"
                }else if (mapname=="杜甫行迹图") {
                    imgurl =window.location.href+"static/img/slide-dufu.gif"
                }else if (mapname=="汤显祖行迹图") {
                    imgurl =window.location.href+"static/img/slide-tangxianzu.gif"
                }else if (mapname=="全宋文专题") {
                    imgurl =window.location.href+"static/img/slide-quansongwen.gif"
                }else if (mapname=="清代妇女作家专题图") {
                    imgurl =window.location.href+"static/img/slide-qingdaifunv.gif"
                }else if (mapname=="全元文专题") {
                    imgurl =window.location.href+"static/img/slide-quanyuanwen.gif"
                }
				*/
            // }
            if(type == "hottest"){
            	$("#"+curdiv).children("p")[0].innerHTML += ("<br>" + gettext("Author:") + username);
            	$("#"+curdiv).children("p")[0].innerHTML += ("<br>" + gettext("Popular Count:") + popularcount);
            }
            else if (type == "latest"){
				$("#"+curdiv).children("p")[0].innerHTML += ("<br>" + gettext("Author:") + username);
            	$("#"+curdiv).children("p")[0].innerHTML += ("<br>" + gettext("Updated Date:") + date);
            }
            img.attr("src",imgurl);
		}
		else
		{
			curdiv = divIdPrefix + (i+1);
			img = $("#"+curdiv).find("img");
			if(typeof($("#"+curdiv).attr("onclick"))!="undefined")
			{
				$("#"+curdiv).removeAttr("onclick");
				$("#"+curdiv).children("p").text("");
				img.attr("src","{{ STATIC_URL }}img/noData.jpg");
			}
		}
	}
}
// get cookie value from cookies
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
function setImgHeight() {
	var imgs = $(".picItem");
	imgs.each(function (i) {
		var img = $(this);
		var width = img.width();
		var height = width* 0.75;
		img.height(height);
	});
    var imgs = $(".item");
    imgs.each(function (i) {
        var img = $(this);
        var width = img.width();
        var height = width* 0.75;
        img.height(height);
    });
}
