/* 定义一个检查数据的方法 */
function check_value(){
  //判断用户输入的用户名和密码不为空
  if($('#username').val().length !=0 && $('#password').val().length!=0){
    //调用jquery的animate方法重新定义CSS
    $('#loginbtn').animate({left:'0', duration:'slow'});//控制登录按钮从左边滑入，通过控制left属性
    $('#lockbtn').animate({left:'260px', duration:'slow'});//同样控制锁定按钮向右滑动消失
  }
}

/* 定义登录按钮出现后点击登录按钮 */
$(function(){
  $('#loginbtn').click(function(){
    //定义回调方法
    $('#loading').removeClass('hidden');//点击登录按钮触发“加载中效果”
  });
});