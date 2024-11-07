clear all
import delimited "C:\Users\samdu\OneDrive\Desktop\Econometrics\Final_Project\data_analysis\scores_formatted2.csv"

xtset year

gen ln_score = log(score)
gen ln_reg_season_points = log(reg_season_points)
gen ln_opp_reg_season_pa = log(opp_reg_season_pa)
gen least_starters_exp_quartile = max(0, 2 - (starters_playoff_exp_quartile))
gen away = 1-at_home
gen least_starters_exp_quartile_away = least_starters_exp_quartile * away
gen total_playoff_exp_dif = starters_playoff_exp_dif + bench_playoff_exp_dif


// //3. NBA Playoff Setting
// //2020 playoffs home court advantage
// reg ln_score ln_reg_season_points ln_opp_reg_season_pa at_home if year == 2020
// outreg2 using 2020.doc, replace ctitle(2020 ln_score)
//
// reg ln_score ln_reg_season_points ln_opp_reg_season_pa at_home if year == 2021
// outreg2 using 2021.doc, replace ctitle(2021 ln_score)

//NBA playoff and regular season scoring averages
// graph bar (mean) score (mean) reg_season_points, over(year, gap(150) label(angle(vertical) labsize(relative2p2)))

//5. Descriptive Stats
pwcorr at_home ln_reg_season_points ln_opp_reg_season_pa starters_playoff_exp_dif

//7. Main Equations
//Base model
xtreg ln_score ln_reg_season_points ln_opp_reg_season_pa away starters_playoff_exp_dif, fe
outreg2 using base.doc, replace title(ln(Playoff Score) Base Model with Starter Exp Difference) addtext(Year FE, YES)

//Testing Starter and Bench exp dif
xtreg ln_score ln_reg_season_points ln_opp_reg_season_pa away starters_playoff_exp_dif bench_playoff_exp_dif, fe
outreg2 using starter_bench.doc, replace title(ln(Playoff Score) with Starter and Bench Exp Difference) addtext(Year FE, YES)

test _b[bench_playoff_exp_dif] = _b[starters_playoff_exp_dif]
outreg2 using bob.doc

preserve

drop if year == 2020
//Least exp starters away
xtreg ln_score ln_reg_season_points ln_opp_reg_season_pa away starters_playoff_exp_dif least_starters_exp_quartile least_starters_exp_quartile_away, fe
outreg2 using least_exp_away.doc, replace title(ln(Playoff Score) with Least Starters Exp Difference Quartile) addtext(Year FE, YES)

test _b[least_starters_exp_quartile_away] = 0

restore