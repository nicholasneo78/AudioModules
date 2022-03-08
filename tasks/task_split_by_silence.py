from clearml import Task, Dataset, TaskTypes

PROJECT_NAME = "audio_preproc_test"
TASK_NAME = "audio_silence_split"
DATASET_POSTFIX = "_sil"
OUTPUT_URL = "s3://experiment-logging/storage"

task = Task.init(project_name=PROJECT_NAME, task_name=TASK_NAME, task_type=TaskTypes.data_processing)
task.set_base_docker(docker_image="dleongsh/audio_preproc:v1.0.0")

args = {
    'dataset_task_id': '',
    'manifest_path': 'manifest.json',
    'thresh': 16,
    'min_silence_len': 500,
}

task.connect(args)
task.execute_remotely()

from preprocessing import SilenceSplitter

# import dataset

dataset = Dataset.get(dataset_id = args['dataset_task_id'])
dataset_path = dataset.get_local_copy()

# process
silence_splitter = SilenceSplitter(
    thresh = args['thresh'],
    min_silence_len = args['min_silence_len']
)

new_dataset_path = silence_splitter(
    input_dir = dataset_path,
    manifest_path = args['manifest_path'],
)

# register ClearML Dataset
clearml_dataset = Dataset.create(
    dataset_project=dataset.project, dataset_name=dataset.name + DATASET_POSTFIX
)
clearml_dataset.add_files(new_dataset_path)
clearml_dataset.upload(output_url=OUTPUT_URL)
clearml_dataset.finalize()

task.set_parameter(
    name="output_dataset_id", 
    value=clearml_dataset.id, 
    description="the dataset task id of the output dataset"
    ) 
print('Done')