﻿var jobCount=0;

function getElement(link){
	var temp=$(".job_name>a")	
	for(i=0 ;i<temp.length;i++){		
		if($(temp[i]).attr("href")==link){return temp[i];}
	}
}

$(document).bind("DOMSubtreeModified", function() {
	// console.log(count%6);
	var linkArray=[];
	
	var x=$(".job_name>a" );
	// console.log("xlength"+x.length);
	// console.log(jobCount);
	if(jobCount!=x.length){

		for(i=0 ;i<x.length;i++){
			// console.log($(x[i]).attr("href"));		
			linkArray.push($(x[i]).attr("href"));
		}
		$.ajax({
				url: "your_link",
				cache: false,
				type: "POST",
				data: JSON.stringify({"linkArray":linkArray}),
				dataType: "json"
			}).done(function(data) {
				//console.log(Object.keys(data).length);
				// console.log(data);
				var obj = JSON.parse(data);
				// console.log("ya--------------------------------------------");
				for(idx=0 ;idx<linkArray.length;idx++){
					var target=getElement(linkArray[idx]);
					// console.log(target);
					var exitDayTemp=0;	
					if(obj[linkArray[idx]]){exitDayTemp = obj[linkArray[idx]];}
					console.log(exitDayTemp);
					switch(true){
						case exitDayTemp>30:
			        		$(target).css("color", "red");
			        		break;
			    		case exitDayTemp>15:
			        		$(target).css("color", "orange");
			        		break;
						case exitDayTemp>0:
			        		$(target).css("color", "green");
					}
				}
			}).fail(function() {
				alert("職缺小幫手讀取失敗");
			});
		jobCount=x.length;
	}
});


