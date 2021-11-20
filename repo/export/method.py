import abc
import pandas
import re

class MethodTypeError(ValueError):
    pass


class MethodInterface(abc.ABC):
    def __init__(self, method):
        self.method = method

    @staticmethod
    def re_split(s):
        res = re.split('([-+]?\d+\.\d+)|([-+]?\d+)', s.strip())
        res_list = [r.strip() for r in res if r is not None and r.strip() != '']
        return res_list

    @abc.abstractmethod
    def concat_df(self, res, tmp, str_info):
        pass

    @abc.abstractmethod
    def concat_meta(self, res, tmp, str_info):
        pass


class Union(MethodInterface):
    def concat_df(self, res, tmp, str_info):
        tmp['wave'] = str_info
        res = pandas.concat([res, tmp], ignore_index=True)
        return res

    def concat_meta(self, res, tmp, str_info):
        tmp_org_type = tmp.original_variable_types
        tmp_var_labels = tmp.variable_value_labels
        tmp_col_names = tmp.column_names
        tmp_col_labels = tmp.column_labels

        for col, col_type in tmp_org_type.items():
            expand=True
            
            if res['org_types'].get(col):
                old_f,old_num = self.re_split(res['org_types'][col])
                new_f,new_num = self.re_split(col_type)
                if float(old_num)>=float(new_num):
                    expand=False

            if expand:
                res['org_types'].update({col : col_type})

        for col, labels in tmp_var_labels.items():
            if res['var_labels'].get(col):
                res['var_labels'][col].update(labels)
            else:
                res['var_labels'][col] = labels

        for i in range(len(tmp_col_names)):
            res['prob_topic'].update({tmp_col_names[i]:tmp_col_labels[i]})
        
        return res


class Join(MethodInterface):
    @staticmethod
    def repl_except(col_name, str_info):
        if col_name == 'baby_id':
            return col_name
        else:
            return f'{col_name}_{str_info}'

    def concat_df(self, res, tmp, str_info):
        tmp.columns = [self.repl_except(c, str_info) for c in tmp.columns]
        if res.empty:
            res = tmp
        else:
            res = res.merge(tmp,
                            on='baby_id',
                            how=self.method,
                            suffixes=(False, f'_{str_info}'))
        return res

    def concat_meta(self, res, tmp, str_info):
        tmp_org_type = tmp.original_variable_types
        tmp_var_labels = tmp.variable_value_labels
        tmp_col_names = tmp.column_names
        tmp_col_labels = tmp.column_labels

        for col, col_type in tmp_org_type.items():
            expand=True
            col_repl = self.repl_except(col, str_info)
            
            if res['org_types'].get(col_repl):
                old_f,old_num = self.re_split(res['org_types'][col_repl])
                new_f,new_num = self.re_split(col_type)
                if float(old_num)>=float(new_num):
                    expand=False

            if expand:
                res['org_types'].update({col_repl : col_type})

        for col, labels in tmp_var_labels.items():
            res['var_labels'].update({f'{col}_{str_info}': labels})

        for i in range(len(tmp_col_labels)):
            res['prob_topic'].update({self.repl_except(tmp_col_names[i], str_info): tmp_col_labels[i]})

        return res


class MethodFactory():
    def __new__(cls, method):
        method_list = ['cross', 'inner', 'outer']
        if method == 'union':
            return Union(method)
        elif method in method_list:
            return Join(method)
        else:
            raise MethodTypeError
