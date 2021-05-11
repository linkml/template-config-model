import os
import unittest

from linkml_runtime.loaders import yaml_loader, json_loader, rdf_loader

from template_config_model.config_model import Config

CWD = os.path.abspath(os.path.dirname(__file__))
INPUT_DIR = os.path.join(CWD, 'input')


class InputFileTestCase(unittest.TestCase):
    """ Test the input files against the model"""
    def test_input_files(self):
        """ Iterate over the input directory loading any test files """
        def gen_detail(total: int, passed: int, typ: str) -> str:
            return f"{total} {typ} files tested - {total-passed} failures"

        nyaml, njson, nttl = 0, 0, 0
        pyaml, pjson, pttl = 0, 0, 0
        nunk = 0
        nread, nfailures = 0, 0
        print('\n\n')
        for dpath, _, files in os.walk(INPUT_DIR):
            for fname in files:
                full_fname = os.path.join(dpath, fname)
                nread += 1
                try:
                    if fname.endswith('.yaml'):
                        nyaml += 1
                        o: Config = yaml_loader.load(full_fname, Config)
                        pyaml += 1
                    elif fname.endswith('.json'):
                        njson += 1
                        o: Config = json_loader.load(full_fname, Config)
                        pjson += 1
                    elif fname.endswith('.ttl'):
                        nttl += 1
                        o: Config = rdf_loader.load(full_fname, Config)
                        pttl += 1
                    elif fname.endswith('.md'):
                        pass
                    else:
                        nunk += 1
                except Exception as e:
                    print(f"----- Error in file {fname} -----")
                    print(str(e))
                    print()
                    nfailures += 1

        print(f"{nread} files tested")
        print(f"\t{nread - nfailures} tests passed ({nfailures} failed)")
        print("\tDetails:")
        print(f"\t\t{gen_detail(nyaml, pyaml, 'YAML')}")
        print(f"\t\t{gen_detail(njson, pjson, 'JSON')}")
        print(f"\t\t{gen_detail(nttl, pttl, 'TTL')}")
        if nunk:
            print(f"{nunk} files of unrecognized type")
        self.assertEqual(0, nfailures)


if __name__ == '__main__':
    unittest.main()
