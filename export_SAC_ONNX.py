from stable_baselines3 import SAC
from stable_baselines3.common.policies import ActorCriticPolicy
import torch as th
from typing import Tuple

class OnnxableSB3SAC(th.nn.Module):
    def __init__(self, actor):
        super().__init__()
        self.actor = th.nn.Sequential(actor.latent_pi, actor.mu)
        #self.actor = actor

    def forward(self, observation: th.Tensor):
        # NOTE: Preprocessing is included, but postprocessing
        # (clipping/inscaling actions) is not,
        #a = self.actor.features_extractor()
        return self.actor(observation)

# Load the state dictionary
model = SAC.load("/app/results/save-08.14.2024_06.39.34/best_model.zip", device="cuda")
print(model.policy)
onnx_sac = OnnxableSB3SAC(model.actor)
observation_size = model.observation_space.shape
print("observation size= ", observation_size)
dummy_input = th.randn(1, *observation_size).to("cuda")

th.onnx.export(
    onnx_sac,
    dummy_input,
    "/app/sac_kin_discrete2d_complex_wo_tanh_436reward.onnx",
    opset_version=17,
    input_names=["input"], 
)

#th.save(onnx_sac.state_dict(), "/app/hovering_sac_kin_discrete2d.pth")

#pytorch_sac = th.load("/app/hovering_sac_kin_discrete2d.pth")


# Post-process: rescale to correct space
# Rescale the action from [-1, 1] to [low, high]
low, high = model.action_space.low, model.action_space.high
print("#####################################################")
#print(model.predict(dummy_input.to("cpu"), deterministic=True))

import onnx
import onnxruntime as ort
import numpy as np

onnx_path = "/app/sac_kin_discrete2d_complex_wo_tanh_436reward.onnx"
onnx_model = onnx.load(onnx_path)
onnx.checker.check_model(onnx_model)

observation = np.zeros((1, *observation_size)).astype(np.float32)
#generate random observation
observation = np.random.rand(1, *observation_size).astype(np.float32)
print(observation)
#custom observation
#observation = np.array([[[0,0,10,0,0,0,2,2,4,1,1,1]]]).astype(np.float32)
ort_sess = ort.InferenceSession(onnx_path)
actions = ort_sess.run(None, {"input": observation})
#post_processed_action = low + (0.5 * (np.array(actions) + 1.0) * (high - low))
print(actions)

print("#####################################################")
# Check that the predictions are the same
with th.no_grad():
    print(model.predict(th.as_tensor(observation), deterministic=True))