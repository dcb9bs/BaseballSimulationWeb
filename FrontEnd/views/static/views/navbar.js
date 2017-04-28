/**
 * Created by Drew on 4/21/17.
 */
$(document).ready(function() {
    $("ul li").click(function() {
        $("ul .active").removeClass("active");
        $(this).addClass("active");
    });
});