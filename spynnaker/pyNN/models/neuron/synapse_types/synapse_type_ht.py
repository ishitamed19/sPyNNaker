from pacman.executor.injection_decorator import inject_items
from spynnaker.pyNN.models.neuron.synapse_types.synapse_type_exponential \
    import get_exponential_decay_and_init

from spynnaker.pyNN.models.neuron.synapse_types.abstract_synapse_type import \
    AbstractSynapseType
from spynnaker.pyNN.utilities import utility_calls
from spynnaker.pyNN.models.neural_properties.neural_parameter \
    import NeuronParameter

from data_specification.enums.data_type import DataType
from enum import Enum
import numpy


class _COMB_EXP_TYPES(Enum):
    SYN_A_RESPONSE = (1, DataType.S1615)
    SYN_A_A = (2, DataType.S1615)
    SYN_A_DECAY = (3, DataType.UINT32)
    SYN_B_RESPONSE = (4, DataType.S1615)
    SYN_B_B = (5, DataType.S1615)
    SYN_B_DECAY = (6, DataType.UINT32)

    def __new__(cls, value, data_type):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._data_type = data_type
        return obj

    @property
    def data_type(self):
        return self._data_type


class SynapseTypeHT(AbstractSynapseType):

    def __init__(self,
                 n_neurons,
                 # excitatory - AMPA
                 exc_a_response,
                 exc_a_A,
                 exc_a_tau,
                 exc_b_response,
                 exc_b_B,
                 exc_b_tau,
                 # excitatory2 - NMDA
                 exc2_a_response,
                 exc2_a_A,
                 exc2_a_tau,
                 exc2_b_response,
                 exc2_b_B,
                 exc2_b_tau,
                 # inhibitory - GABA_A
                 inh_a_response,
                 inh_a_A,
                 inh_a_tau,
                 inh_b_response,
                 inh_b_B,
                 inh_b_tau,
                 # inhibitory2 - GABA_B
                 inh2_a_response,
                 inh2_a_A,
                 inh2_a_tau,
                 inh2_b_response,
                 inh2_b_B,
                 inh2_b_tau,
                 ):

        AbstractSynapseType.__init__(self)
        self._n_neurons = n_neurons

        # excitatory
        self._exc_a_response = \
            utility_calls.convert_param_to_numpy(exc_a_response, n_neurons)
        self._exc_a_A = \
            utility_calls.convert_param_to_numpy(exc_a_A, n_neurons)
        self._exc_a_tau = \
            utility_calls.convert_param_to_numpy(exc_a_tau, n_neurons)
        self._exc_b_response = \
            utility_calls.convert_param_to_numpy(exc_b_response, n_neurons)
        self._exc_b_B = \
            utility_calls.convert_param_to_numpy(exc_b_B, n_neurons)
        self._exc_b_tau = \
            utility_calls.convert_param_to_numpy(exc_b_tau, n_neurons)

        self.exc_a_A, self.exc_b_B = \
            set_excitatory_scalar(self._exc_a_tau, self._exc_b_tau)

        # excitatory2
        self._exc2_a_response = \
            utility_calls.convert_param_to_numpy(exc2_a_response, n_neurons)
        self._exc2_a_A = \
            utility_calls.convert_param_to_numpy(exc2_a_A, n_neurons)
        self._exc2_a_tau = \
            utility_calls.convert_param_to_numpy(exc2_a_tau, n_neurons)
        self._exc2_b_response = \
            utility_calls.convert_param_to_numpy(exc2_b_response, n_neurons)
        self._exc2_b_B = \
            utility_calls.convert_param_to_numpy(exc2_b_B, n_neurons)
        self._exc2_b_tau = \
            utility_calls.convert_param_to_numpy(exc2_b_tau, n_neurons)

        self.exc2_a_A, self.exc2_b_B = \
            set_excitatory_scalar(self._exc2_a_tau, self._exc2_b_tau)

        # inhibitory
        self._inh_a_response = \
            utility_calls.convert_param_to_numpy(inh_a_response, n_neurons)
        self._inh_a_A = \
            utility_calls.convert_param_to_numpy(inh_a_A, n_neurons)
        self._inh_a_tau = \
            utility_calls.convert_param_to_numpy(inh_a_tau, n_neurons)
        self._inh_b_response = \
            utility_calls.convert_param_to_numpy(inh_b_response, n_neurons)
        self._inh_b_B = \
            utility_calls.convert_param_to_numpy(inh_b_B, n_neurons)
        self._inh_b_tau = \
            utility_calls.convert_param_to_numpy(inh_b_tau, n_neurons)

        self._inh_a_A, self._inh_b_B = \
            set_excitatory_scalar(self._inh_a_tau, self._inh_b_tau)

        # inhibitory2
        self._inh2_a_response = \
            utility_calls.convert_param_to_numpy(inh2_a_response, n_neurons)
        self._inh2_a_A = \
            utility_calls.convert_param_to_numpy(inh2_a_A, n_neurons)
        self._inh2_a_tau = \
            utility_calls.convert_param_to_numpy(inh2_a_tau, n_neurons)
        self._inh2_b_response = \
            utility_calls.convert_param_to_numpy(inh2_b_response, n_neurons)
        self._inh2_b_B = \
            utility_calls.convert_param_to_numpy(inh2_b_B, n_neurons)
        self._inh2_b_tau = \
            utility_calls.convert_param_to_numpy(inh2_b_tau, n_neurons)

        self._inh2_a_A, self._inh2_b_B = \
            set_excitatory_scalar(self._inh2_a_tau, self._inh2_b_tau)

    # excitatory
    @property
    def exc_a_response(self):
        return self._exc_a_response

    @exc_a_response.setter
    def exc_a_response(self, exc_a_response):
        self._exc_a_response = utility_calls.convert_param_to_numpy(
            exc_a_response, self._n_neurons)

    @property
    def exc_a_A(self):
        return self._exc_a_A

    @exc_a_A.setter
    def exc_a_A(self, exc_a_A):
        self._exc_a_A = utility_calls.convert_param_to_numpy(
            exc_a_A, self._n_neurons)

    @property
    def exc_a_tau(self):
        return self._exc_a_tau

    @exc_a_tau.setter
    def exc_a_tau(self, exc_a_tau):
        self._exc_a_tau = utility_calls.convert_param_to_numpy(
            exc_a_tau, self._n_neurons)
        self.exc_a_A, self.exc_b_B = \
            set_excitatory_scalar(self._exc_a_tau, self._exc_b_tau)

    @property
    def exc_b_response(self):
        return self._exc_b_response

    @exc_b_response.setter
    def exc_b_response(self, exc_b_response):
        self._exc_b_response = utility_calls.convert_param_to_numpy(
            exc_b_response, self._n_neurons)

    @property
    def exc_b_B(self):
        return self._exc_b_B

    @exc_b_B.setter
    def exc_b_B(self, exc_b_B):
        self._exc_b_B = utility_calls.convert_param_to_numpy(
            exc_b_B, self._n_neurons)

    @property
    def exc_b_tau(self):
        return self._exc_b_tau

    @exc_b_tau.setter
    def exc_b_tau(self, exc_b_tau):
        self._exc_b_tau = utility_calls.convert_param_to_numpy(
            exc_b_tau, self._n_neurons)
        self.exc_a_A, self.exc_b_B = \
            set_excitatory_scalar(self._exc_a_tau, self._exc_b_tau)

    # excitatory2
    @property
    def exc2_a_response(self):
        return self._exc2_a_response

    @exc2_a_response.setter
    def exc2_a_response(self, exc2_a_response):
        self._exc2_a_response = utility_calls.convert_param_to_numpy(
            exc2_a_response, self._n_neurons)

    @property
    def exc2_a_A(self):
        return self._exc2_a_A

    @exc2_a_A.setter
    def exc2_a_A(self, exc2_a_A):
        self._exc2_a_A = utility_calls.convert_param_to_numpy(
            exc2_a_A, self._n_neurons)

    @property
    def exc2_a_tau(self):
        return self._exc2_a_tau

    @exc2_a_tau.setter
    def exc2_a_tau(self, exc2_a_tau):
        self._exc2_a_tau = utility_calls.convert_param_to_numpy(
            exc2_a_tau, self._n_neurons)
        self.exc2_a_A, self.exc2_b_B = \
            set_excitatory_scalar(self._exc2_a_tau, self._exc2_b_tau)

    @property
    def exc2_b_response(self):
        return self._exc2_b_response

    @exc2_b_response.setter
    def exc2_b_response(self, exc2_b_response):
        self._exc2_b_response = utility_calls.convert_param_to_numpy(
            exc2_b_response, self._n_neurons)

    @property
    def exc2_b_B(self):
        return self._exc2_b_B

    @exc2_b_B.setter
    def exc2_b_B(self, exc2_b_B):
        self._exc2_b_B = utility_calls.convert_param_to_numpy(
            exc2_b_B, self._n_neurons)

    @property
    def exc2_b_tau(self):
        return self._exc2_b_tau

    @exc2_b_tau.setter
    def exc2_b_tau(self, exc2_b_tau):
        self._exc2_b_tau = utility_calls.convert_param_to_numpy(
            exc2_b_tau, self._n_neurons)
        self.exc2_a_A, self.exc2_b_B = \
            set_excitatory_scalar(self._exc2_a_tau, self._exc2_b_tau)

    # inhibitory
    @property
    def inh_a_response(self):
        return self._inh_a_response

    @inh_a_response.setter
    def inh_a_response(self, inh_a_response):
        self._inh_a_response = utility_calls.convert_param_to_numpy(
            inh_a_response, self._n_neurons)

    @property
    def inh_a_A(self):
        return self._inh_a_A

    @inh_a_A.setter
    def inh_a_A(self, inh_a_A):
        self._inh_a_A = utility_calls.convert_param_to_numpy(
            inh_a_A, self._n_neurons)

    @property
    def inh_a_tau(self):
        return self._inh_a_tau

    @inh_a_tau.setter
    def inh_a_tau(self, inh_a_tau):
        self._inh_a_tau = utility_calls.convert_param_to_numpy(
            inh_a_tau, self._n_neurons)
        self._inh_a_A, self._inh_b_B = \
            set_excitatory_scalar(self._inh_a_tau, self._inh_b_tau)

    @property
    def inh_b_response(self):
        return self._inh_b_response

    @inh_b_response.setter
    def inh_b_response(self, inh_b_response):
        self._inh_b_response = utility_calls.convert_param_to_numpy(
            inh_b_response, self._n_neurons)

    @property
    def inh_b_B(self):
        return self._inh_b_B

    @inh_b_B.setter
    def inh_b_B(self, inh_b_B):
        self._inh_b_B = utility_calls.convert_param_to_numpy(
            inh_b_B, self._n_neurons)

    @property
    def inh_b_tau(self):
        return self._inh_b_tau

    @inh_b_tau.setter
    def inh_b_tau(self, inh_b_tau):
        self._inh_b_tau = utility_calls.convert_param_to_numpy(
            inh_b_tau, self._n_neurons)
        self._inh_a_A, self._inh_b_B = \
            set_excitatory_scalar(self._inh_a_tau, self._inh_b_tau)

    # inhibitory2
    @property
    def inh2_a_response(self):
        return self._inh2_a_response

    @inh2_a_response.setter
    def inh2_a_response(self, inh2_a_response):
        self._inh2_a_response = utility_calls.convert_param_to_numpy(
            inh2_a_response, self._n_neurons)

    @property
    def inh2_a_A(self):
        return self._inh2_a_A

    @inh2_a_A.setter
    def inh2_a_A(self, inh2_a_A):
        self._inh2_a_A = utility_calls.convert_param_to_numpy(
            inh2_a_A, self._n_neurons)

    @property
    def inh2_a_tau(self):
        return self._inh2_a_tau

    @inh2_a_tau.setter
    def inh2_a_tau(self, inh2_a_tau):
        self._inh2_a_tau = utility_calls.convert_param_to_numpy(
            inh2_a_tau, self._n_neurons)
        self._inh2_a_A, self._inh2_b_B = \
            set_excitatory_scalar(self._inh2_a_tau, self._inh2_b_tau)

    @property
    def inh2_b_response(self):
        return self._inh2_b_response

    @inh2_b_response.setter
    def inh2_b_response(self, inh2_b_response):
        self._inh2_b_response = utility_calls.convert_param_to_numpy(
            inh2_b_response, self._n_neurons)

    @property
    def inh2_b_B(self):
        return self._inh2_b_B

    @inh2_b_B.setter
    def inh2_b_B(self, inh2_b_B):
        self._inh2_b_B = utility_calls.convert_param_to_numpy(
            inh2_b_B, self._n_neurons)

    @property
    def inh2_b_tau(self):
        return self._inh2_b_tau

    @inh2_b_tau.setter
    def inh2_b_tau(self, inh2_b_tau):
        self._inh2_b_tau = utility_calls.convert_param_to_numpy(
            inh2_b_tau, self._n_neurons)
        self._inh2_a_A, self._inh2_b_B = \
            set_excitatory_scalar(self._inh2_a_tau, self._inh2_b_tau)

    def get_n_synapse_types(self):
        return 4  # AMPA, NMDA, GABA_A, GABA_B

    def get_synapse_id_by_target(self, target):

        if target == "AMPA":
            return 0
        elif target == "NMDA":
            return 1
        elif target == "GABA_A":
            return 2
        elif target == "GABA_B":
            return 3
        return None

    def get_synapse_targets(self):
        return "AMPA", "NMDA", "GABA_A", "GABA_B"

    def get_n_synapse_type_parameters(self):
        return self.get_n_synapse_types() * 6

    @inject_items({"machine_time_step": "MachineTimeStep"})
    def get_synapse_type_parameters(self, machine_time_step):

        # excitatory
        e_a_decay, e_a_init = get_exponential_decay_and_init(
            self._exc_a_tau, machine_time_step)
        e_b_decay, e_b_init = get_exponential_decay_and_init(
            self._exc_b_tau, machine_time_step)

        # excitatory2
        e2_a_decay, e2_a_init = get_exponential_decay_and_init(
            self._exc2_a_tau, machine_time_step)
        e2_b_decay, e2_b_init = get_exponential_decay_and_init(
            self._exc2_b_tau, machine_time_step)

        # inhibitory
        i_a_decay, i_a_init = get_exponential_decay_and_init(
            self._inh_a_tau, machine_time_step)
        i_b_decay, i_b_init = get_exponential_decay_and_init(
            self._inh_b_tau, machine_time_step)

        # inhibitory2
        i2_a_decay, i2_a_init = get_exponential_decay_and_init(
            self._inh2_a_tau, machine_time_step)
        i2_b_decay, i2_b_init = get_exponential_decay_and_init(
            self._inh2_b_tau, machine_time_step)

        return [
            # excitatory
            NeuronParameter(self._exc_a_response,
                            _COMB_EXP_TYPES.SYN_A_RESPONSE.data_type),
            NeuronParameter(self._exc_a_A, _COMB_EXP_TYPES.SYN_A_A.data_type),
            NeuronParameter(e_a_decay, _COMB_EXP_TYPES.SYN_A_DECAY.data_type),

            NeuronParameter(self._exc_b_response,
                            _COMB_EXP_TYPES.SYN_B_RESPONSE.data_type),
            NeuronParameter(self._exc_b_B, _COMB_EXP_TYPES.SYN_B_B.data_type),
            NeuronParameter(e_b_decay, _COMB_EXP_TYPES.SYN_B_DECAY.data_type),

            # excitatory2
            NeuronParameter(self._exc2_a_response,
                            _COMB_EXP_TYPES.SYN_A_RESPONSE.data_type),
            NeuronParameter(self._exc2_a_A, _COMB_EXP_TYPES.SYN_A_A.data_type),
            NeuronParameter(e2_a_decay, _COMB_EXP_TYPES.SYN_A_DECAY.data_type),

            NeuronParameter(self._exc2_b_response,
                            _COMB_EXP_TYPES.SYN_B_RESPONSE.data_type),
            NeuronParameter(self._exc2_b_B, _COMB_EXP_TYPES.SYN_B_B.data_type),
            NeuronParameter(e2_b_decay, _COMB_EXP_TYPES.SYN_B_DECAY.data_type),

            # inhibitory
            NeuronParameter(self._inh_a_response,
                            _COMB_EXP_TYPES.SYN_A_RESPONSE.data_type),
            NeuronParameter(self._inh_a_A, _COMB_EXP_TYPES.SYN_A_A.data_type),
            NeuronParameter(i_a_decay, _COMB_EXP_TYPES.SYN_A_DECAY.data_type),

            NeuronParameter(self._inh_b_response,
                            _COMB_EXP_TYPES.SYN_B_RESPONSE.data_type),
            NeuronParameter(self._inh_b_B, _COMB_EXP_TYPES.SYN_B_B.data_type),
            NeuronParameter(i_b_decay, _COMB_EXP_TYPES.SYN_B_DECAY.data_type),

            # inhibitory2
            NeuronParameter(self._inh2_a_response,
                            _COMB_EXP_TYPES.SYN_A_RESPONSE.data_type),
            NeuronParameter(self._inh2_a_A, _COMB_EXP_TYPES.SYN_A_A.data_type),
            NeuronParameter(i2_a_decay, _COMB_EXP_TYPES.SYN_A_DECAY.data_type),

            NeuronParameter(self._inh2_b_response,
                            _COMB_EXP_TYPES.SYN_B_RESPONSE.data_type),
            NeuronParameter(self._inh2_b_B, _COMB_EXP_TYPES.SYN_B_B.data_type),
            NeuronParameter(i2_b_decay, _COMB_EXP_TYPES.SYN_B_DECAY.data_type)
        ]

    def get_synapse_type_parameter_types(self):

        # TODO: update to return the parameter types
        return [item.data_type for item in _COMB_EXP_TYPES]

    def get_n_cpu_cycles_per_neuron(self):
        # a guess
        return 100


def calc_rise_time(tau_a, tau_b, A=1, B=-1):
    try:
        return numpy.log((A*tau_b) / (-B*tau_a)) * (
            (tau_a*tau_b) / (tau_b - tau_a))
    except:
        "calculation failed: ensure A!=B and that they are of opposite sign"
        return None


def calc_scalar_f(tau_a, tau_b):
    t_rise = calc_rise_time(tau_a=tau_a, tau_b=tau_b)
    return 1/(numpy.exp(-t_rise/tau_a) - numpy.exp(-t_rise/tau_b))


def set_excitatory_scalar(exc_a_tau, exc_b_tau):
    sf = calc_scalar_f(tau_a=exc_a_tau, tau_b=exc_b_tau)
    a_A = sf
    b_B = -sf
    return a_A, b_B
