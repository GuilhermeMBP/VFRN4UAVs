# VFRN4UAVs

## Using Docker
### Building
```bash
docker build -t vfrn .
```
### Running
```bash
docker run -it --gpus=all --net=host --env DISPLAY=$DISPLAY vfrn
```

### Post-run
When using vscode dev-containers verify if the cpu is going to 100%, if so try this inside the container:
```bash
ps aux | grep @vs
```
and kill the process that appears in the list

### Running the project
#### Using conda env "drones":
```bash
conda activate drones
```
Running the train of the UAV (at the moment, this is using mysql to run multiple iterations in optuna and there is the need to create the db before this can be run)
```bash
python /app/gym-pybullet-drones/gym_pybullet_drones/examples/learn.py --gui false --record_video false
```
Visualize the control
```bash
python /app/gym-pybullet-drones/gym_pybullet_drones/examples/just_visualize.py --gui false --record_video false
```
Generate the dataset
```bash
python /app/gym-pybullet-drones/gym_pybullet_drones/examples/dataset_generator.py --x 0 --y <starting_point_y> --z <starting_point_z> --step <step (negative value, if it starts in the right or up part)> --step_axis <axis that is used with step for dataset record>
```
Generate vnnlib and vis dataset
```bash
python /app/gym-pybullet-drones/gym_pybullet_drones/examples/dataset_generator.py --obs kin --act discrete_2d_complex --dataset_folder <dataset_folder, ex: /app/VFRN4UAVs/discrete/datasets/dataset_31.08.2024/19.14.17> --perturb <perturbation radius, ex: 0.01> --output_condition quadrants --visualize_dataset True --visualize_actions True
```
#### Activate alpha-beta-crown env
```bash
conda activate alpha-beta-crown
```
Launch alpha-beta-crown verification
```bash
python /app/alpha-beta-CROWN/complete_verifier/abcrown.py --config /app/VFRN4UAVs/discrete/abcrown_yaml/onnx_sac_discrete_multiple_vnnlibs_reward440.yaml
```
#### Activate the conda env drones again!
```bash
conda activate drones
```
Plot the certified and violated points in alpha-beta-crown
```bash
python /app/VFRN4UAVs/plot_certification.py --file_path /app/certified.txt --directory /app/VFRN4UAVs/discrete/datasets/dataset_31.08.2024/final --include_unsafe True
```

Plot the counter examples and the action
```bash
python /app/VFRN4UAVs/plot_cex.py --directory /app/VFRN4UAVs/discrete/datasets/dataset_31.08.2024/final/vnnlibs_0.01_quadrants
```
#### Activate the conda env pynever
```bash
conda activate pynever
```
Verify with pynever. the file exp_launcher needs to be changed for new datasets
```bash
python /app/VFRN4UAVs/pyNever/exp_launcher.py 1 60
```

#### Activate the conda env drones again!
```bash
conda activate drones
```

Plot certified in pynever
```bash
python /app/VFRN4UAVs/pyNever/exp_launcher.py --results_path /app/VFRN4UAVs/pyNever/logs/experiments_too_tilted_436.csv --directory /app/VFRN4UAVs/discrete/datasets/dataset_20.08.2024/final
```
