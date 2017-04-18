/**
 * Created by Drew on 4/15/17.
 */
$(document).ready(function() {
    $("#away_team_select").change(function(){
        var id = $(this).find(":selected").val();
        $.get("/updateTeamSelect/" + id, function(data){
            var i, j;
            var team = data['batters'];
            for(j = 1; j < 10; j++){
                var batter = "#away_batter_" + j;
                $(batter).empty();
                var append_string = "<select>";
                for(i = 0; i < team.length; i++){
                    append_string = append_string + "<option value='" + team[i]['id'] + "'>" + team[i]['full_name'] +
                        "</option>";
                }
                append_string = append_string + "</select>";
                $(batter).append(append_string);
            }
            team = data['pitchers'];
            var pitcher = "#away_pitcher_select";
            $(pitcher).empty();
            var append_string = "";
            for(i = 0; i < team.length; i++){
                append_string = append_string + "<option value='" + team[i]['id'] + "'>" + team[i]['full_name'] +
                    "</option>";
            }
            append_string = append_string + "";
            $(pitcher).append(append_string);

        }, "json");
    });

    $("#home_team_select").change(function(){
        var id = $(this).find(":selected").val();
        $.get("/updateTeamSelect/" + id, function(data){
            var k, l;
            var t = data['batters'];
            for(k = 1; k < 10; k++){
                var name = "#home_batter_" + k;
                $(name).empty();
                var append_string = "<select>";
                for(l = 0; l < t.length; l++){
                    append_string = append_string + "<option value='" + t[l]['id'] + "'>" + t[l]['full_name'] +
                        "</option>";
                }
                append_string = append_string + "</select>";
                $(name).append(append_string);
            }
            t = data['pitchers'];
            var pitcher = "#home_pitcher_select";
            $(pitcher).empty();
            var append_string = "";
            for(l = 0; l < t.length; l++){
                append_string = append_string + "<option value='" + t[l]['id'] + "'>" + t[l]['full_name'] +
                    "</option>";
            }
            append_string = append_string + "";
            $(pitcher).append(append_string);
        }, "json");
    });


});