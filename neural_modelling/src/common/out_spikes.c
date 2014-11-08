#include "out_spikes.h"

#include <bit_field.h>
#include <debug.h>

// Globals
bit_field_t out_spikes;

static size_t out_spikes_size;

void out_spikes_reset() {
    clear_bit_field(out_spikes, out_spikes_size);
}

void out_spikes_initialize(size_t max_spike_sources) {
    out_spikes_size = get_bit_field_size(max_spike_sources);
    log_info("Out spike size is %u words, allowing %u spike sources",
            out_spikes_size, max_spike_sources);

    out_spikes = (bit_field_t) sark_alloc(out_spikes_size * sizeof(uint32_t),
            1);
    reset_out_spikes();
}

void out_spikes_record() {

    // If we should record the spike history, copy out-spikes to the
    // appropriate recording channel
    if (system_data_test_bit(e_system_data_record_spike_history)) {
        recording_record(e_recording_channel_spike_history, out_spikes,
                out_spikes_size * sizeof(uint32_t));
    }
}

bool out_spikes_is_empty() {
    return (empty_bit_field(out_spikes, out_spikes_size));

}

bool out_spikes_is_nonempty() {
    return (nonempty_bit_field(out_spikes, out_spikes_size));

}

bool out_spikes_is_spike(index_t neuron_index) {
    return (bit_field_test(out_spikes, neuron_index));
}

#if LOG_LEVEL >= LOG_DEBUG
void out_spikes_print() {
    log_debug("out_spikes:\n");

    if (nonempty_out_spikes()) {
        log_debug("-----------\n");
        print_bit_field(out_spikes, out_spikes_size);
        log_debug("-----------\n");
    }
}
#else
void out_spikes_print() {
    skip();
}
#endif  // DEBUG
