import readline
import cmd
import shlex
import pynames
import pkgutil


class Cool_names_cmd(cmd.Cmd):
    """Cool commandline!"""
    intro = "Ryan Gosling. Drive"
    prompt = "<3 "
    lang = pynames.LANGUAGE.NATIVE
    info_buf = ['male', 'female', 'language']
    if True:
        gens = [module_name for _, module_name, _ in pkgutil.iter_modules([pynames.generators.generators_root])]
        subgens = {gen_name: {subgen_name.replace("NamesGenerator", "").replace("FullnameGenerator", ""): gen
                              for subgen_name, gen in pynames.generators.__dict__[gen_name].__dict__.items()
                              if subgen_name.endswith("NamesGenerator") or subgen_name.endswith("FullnameGenerator")}
                   for gen_name in gens}
        
        simple_gens = dict(map(lambda x: x if len(x[1]) == 1 else (x[0], {}), subgens.items()))
        compl_gens = dict(map(lambda x: x if len(x[1]) > 1 else (x[0], {}), subgens.items()))


    def do_language(self, args):
        """Language switch"""
        lang = shlex.split(args)
        if len(lang) != 1:
            print("Wrong number of arguments")
        elif lang[0] not in pynames.LANGUAGE.ALL:
            print(f"The {lang[0]} language is not supported")
        else:
            self.lang = lang[0]


    def do_generate(self, args):
        params = shlex.split(args)
        gender = pynames.GENDER.MALE
        match len(params):
            case 3:
                gen_name, buf, gender = params
                subclass = self.compl_gens[gen_name] if len(self.simple_gens[gen_name]) == 0 else self.simple_gens[gen_name]
                gen_class = subclass[buf]
            case 2:
                gen_name = params[0]
                subclass = self.compl_gens[gen_name] if len(self.simple_gens[gen_name]) == 0 else self.simple_gens[gen_name]
                if params[1].upper() in ["MALE", "FEMALE"]:
                    gender = params[1].upper()
                    gen_class = [*subclass.values()][0]
                else:
                    gen_class = subclass[params[1]]
            case 1:
                gen_name = params[0]
                subclass = self.compl_gens[gen_name] if len(self.simple_gens[gen_name]) == 0 else self.simple_gens[gen_name]
                gen_class = [*subclass.values()][0]
            case _:
                print("Wrong number of arguments")
        if gender.upper() == "FEMALE":
            gender = pynames.GENDER.FEMALE
        else:
            gender = pynames.GENDER.MALE
        cur_language = self.lang if self.lang in gen_class().languages else pynames.LANGUAGE.NATIVE
        print(gen_class().get_name_simple(gender, cur_language))
        # print(gen_class.language)


    def do_info(self, args):
        params = shlex.split(args)
        
        if len(params) == 3 or (len(params) == 2 and params[1] not in {"language" ,"female", "male"}):
            gen_name = params[0]
            subclass = self.compl_gens[gen_name] if len(self.simple_gens[gen_name]) == 0 else self.simple_gens[gen_name]
            gen_class = [subclass[params[1]]]
        else:
            gen_name = params[0]
            subclass = self.compl_gens[gen_name] if len(self.simple_gens[gen_name]) == 0 else self.simple_gens[gen_name]
            gen_class = [*subclass.values()]

        names_sum = 0
        match params[-1]:
            case "language":
                print(*gen_class().languages)
            case "female":
                for gen in gen_class:
                    names_sum += gen().get_names_number(pynames.GENDER.FEMALE)
                print(names_sum)
            case "male":
                for gen in gen_class:
                    names_sum += gen().get_names_number(pynames.GENDER.MALE)
                print(names_sum)
            case _:
                for gen in gen_class:
                    names_sum += gen().get_names_number()
                print(names_sum)

    
    def do_exit(self, args):
        """Exit programm"""
        return True


    def do_EOF(self, args):
        """Exit programm"""
        return True


    def complete_language(self, prefix, allcmd, beg, end):
        """Completion of the language programm"""
        return [s for s in pynames.LANGUAGE.ALL if s.startswith(prefix)]


    def complete_info(self, prefix, allcmd, beg, end):
        """Completion of info"""
        params = shlex.split(allcmd)
        arg_num = len(params)
        
        if arg_num == 1 or len(shlex.split(allcmd)) == 2 and prefix != '':
            return list(filter(lambda x: x.startswith(prefix), self.simple_gens))
        elif arg_num == 2 or len(shlex.split(allcmd)) == 3 and prefix != '':
            if params[1] in self.simple_gens:
                return list(filter(lambda x: x.startswith(prefix), self.compl_gens),
                            filter(lambda x: x.startswith(prefix), self.info_buf))
            else:
                return list(filter(lambda x: x.startswith(prefix), self.info_buf))
        else:
            return []

    def complete_generate(self, prefix, allcmd, beg, end):
        """Completion of generate"""
        params = shlex.split(allcmd)
        arg_num = len(params)
        
        if arg_num == 1 or len(shlex.split(allcmd)) == 2 and prefix != '':
            return list(filter(lambda x: x.startswith(prefix), self.simple_gens))
        elif arg_num == 2 or len(shlex.split(allcmd)) == 3 and prefix != '':
            if params[1] in self.simple_gens:
                return list(filter(lambda x: x.startswith(prefix), self.compl_gens))
            else:
                return []
        else:
            return []
        


if __name__ == "__main__":
    Cool_names_cmd().cmdloop()
