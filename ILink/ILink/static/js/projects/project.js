/**
 * Created by june on 16/5/12.
 */
$(function() {
    $( "ul.droptrue" ).sortable({
        connectWith: "ul"
    });

    $( "ul.dropfalse" ).sortable({
    connectWith: "ul",
    dropOnEmpty: false
    });

    $( "#sortable1, #sortable2, #sortable3" ).disableSelection();
    });

function checkboxOnclick(checkbox){

    if ( checkbox.checked == true){
        var len = document.getElementById('sortable3').innerHTML+='<li class="li_style">' + '<div class="panel panel-default " style="margin-right:10px"> '+
        '<div class="panel-body-task" >'
        + '<div class="checkbox c-checkbox col-md-8">'
        + '<label>'
        + '<input type="checkbox"  value="">'
        + ' <span class="fa fa-check"></span>'
        +     '<a id="modal-7" href="#modal-container-7" role="button" class="btn_p" data-toggle="modal">'+'任务1'+'</a>'
        +'</label>'
        +'</div>'
       +' <div class="">'
        +'<a href="#" class="btn" align="right">'+'<i class="fa fa-times">'+'</i>'+'</a>'
       + '</div>'
        +'</div>'
        +'</div>'

        +'</li>'


    }else{

    }

}

$(function(){
    $(".btn").click(function(){
        $("#mymodal").modal("toggle");
    });
});

$(".form_datetime").datetimepicker({
    format: "dd MM yyyy - HH:ii P",
    showMeridian: true,
    autoclose: true,
    todayBtn: true
    });


