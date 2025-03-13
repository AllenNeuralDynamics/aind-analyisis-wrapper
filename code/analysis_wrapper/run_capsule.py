import utils

if __name__ == '__main__':
    input_json = utils.read_input_json()
    nwb = utils.read_nwb_from_s3(input_json['s3_location'])
    pass
