# from typing import List
import pyreadstat
import pandas
import os
from ..manager import SQLManager
from .format import FormatFactory
from .method import MethodFactory
from ..utils import AGE_TYPE, SURVEY_TYPE


class SurveyNotFound(FileNotFoundError):
    pass


class MergeManager(SQLManager):
    def __init__(self, method_type: str, format_type: str, wave: str):
        self.method = MethodFactory(method_type)
        self.format = FormatFactory(format_type)
        self.wave = wave
        super().__init__()

    @staticmethod
    def get_str_info(survey_info):
        str_age = AGE_TYPE.inv[survey_info[0]]
        str_survey = SURVEY_TYPE.inv[survey_info[1]]
        str_wave = str(survey_info[2])
        return '_'.join([str_age, str_survey, str_wave])

    def merger(self, account_id: int, upload_path: str,
               destination: str) -> bool:
        # get shop_cart info
        command = (
            "SELECT age_type, survey_type, wave, problem.problem_name "
            "FROM ( "
            "( SELECT survey_id, problem_id FROM dbo.shop_cart WHERE account_id = %(account_id)s) AS alpha "
            "INNER JOIN dbo.survey ON alpha.survey_id = survey.survey_id) "
            "INNER JOIN dbo.problem ON alpha.problem_id = problem.problem_id;")

        shop_cart_survey_problems = pandas.read_sql(
            command, self.conn, params={'account_id': account_id})

        survey_group = shop_cart_survey_problems.groupby(
            ['age_type', 'survey_type', 'wave'])

        res_df = pandas.DataFrame()
        res_meta = {'var_labels': {}, 'org_types': {}, 'prob_topic': {}}


        if self.method.method == 'left':
            for keys, prob_df in survey_group:
                k_age, k_survey, k_wave = keys
                if k_wave == self.wave:
                    unionMethod = MethodFactory('union')
                    prob_df = prob_df.append({'problem_name': 'baby_id'},
                                             ignore_index=True)
                    
                    file_path = os.path.join(upload_path, str(k_age), str(k_survey),
                                             str(k_wave) + '.sav')
    
                    # check file exists
                    if not os.path.isfile(file_path):
                        raise SurveyNotFound
    
                    tmp_df, tmp_meta = pyreadstat.read_sav(
                        file_path,
                        usecols=prob_df['problem_name'].tolist(),
                        disable_datetime_conversion=True)
                    str_info = self.get_str_info(keys)
                    res_df = unionMethod.concat_df(res_df, tmp_df, str_info)
                    res_meta = unionMethod.concat_meta(res_meta, tmp_meta, str_info)


            for keys, prob_df in survey_group:
                k_age, k_survey, k_wave = keys
                if k_wave != self.wave:
                    prob_df = prob_df.append({'problem_name': 'baby_id'},
                                             ignore_index=True)
                    
                    file_path = os.path.join(upload_path, str(k_age), str(k_survey),
                                             str(k_wave) + '.sav')

                    # check file exists
                    if not os.path.isfile(file_path):
                        raise SurveyNotFound

                    tmp_df, tmp_meta = pyreadstat.read_sav(
                        file_path,
                        usecols=prob_df['problem_name'].tolist(),
                        disable_datetime_conversion=True)
                    str_info = self.get_str_info(keys)
                    res_df = self.method.concat_df(res_df, tmp_df, str_info)
                    res_meta = self.method.concat_meta(res_meta, tmp_meta, str_info)


            wave_name = res_df.at[0, "wave"]
            
            for i in range(len(res_df.columns.values)):
                if res_df.columns.values[i] != "baby_id" and res_df.columns.values[i] != "wave":
                    res_df.columns.values[i] = res_df.columns.values[i] + "_" + wave_name
                elif res_df.columns.values[i] == "wave":
                    break

            # del res_df['wave']

        else:
            for keys, prob_df in survey_group:
                k_age, k_survey, k_wave = keys
                prob_df = prob_df.append({'problem_name': 'baby_id'},
                                         ignore_index=True)
                
                file_path = os.path.join(upload_path, str(k_age), str(k_survey),
                                         str(k_wave) + '.sav')

                # check file exists
                if not os.path.isfile(file_path):
                    raise SurveyNotFound

                tmp_df, tmp_meta = pyreadstat.read_sav(
                    file_path,
                    usecols=prob_df['problem_name'].tolist(),
                    disable_datetime_conversion=True)
                str_info = self.get_str_info(keys)
                res_df = self.method.concat_df(res_df, tmp_df, str_info)
                res_meta = self.method.concat_meta(res_meta, tmp_meta, str_info)


        self.format.write(res_df, res_meta, destination)
