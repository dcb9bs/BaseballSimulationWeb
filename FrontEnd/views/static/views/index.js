/**
 * Created by Drew on 4/15/17.
 */
$(document).ready(function() {
    $("#away_team_select").change(function(){
        var id = $(this).find(":selected").val();
        $.get("/updateTeamSelect/" + id, function(data){
            var i, j;
            var team = data['team'];
            for(j = 1; j < 10; j++){
                var name = "#away_player" + j;
                $(name).empty();
                var append_string = "<select>";
                for(i = 0; i < team.length; i++){
                    append_string = append_string + "<option value='" + team[i]['id'] + "'>" + team[i]['full_name'] +
                        "</option>";
                }
                append_string = append_string + "</select>";
                $(name).append(append_string);
            }
        }, "json");
    });

    $("#home_team_select").change(function(){
        var id = $(this).find(":selected").val();
        $.get("/updateTeamSelect/" + id, function(data){
            var i, j;
            var team = data['team'];
            for(j = 1; j < 10; j++){
                var name = "#home_player" + j;
                $(name).empty();
                var append_string = "<select>";
                for(i = 0; i < team.length; i++){
                    append_string = append_string + "<option value='" + team[i]['id'] + "'>" + team[i]['full_name'] +
                        "</option>";
                }
                append_string = append_string + "</select>";
                $(name).append(append_string);
            }
        }, "json");
    });


});