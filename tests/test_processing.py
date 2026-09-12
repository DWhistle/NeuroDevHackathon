import json
import unittest

from examples.generate_packets import generate_packets
from model_builder import build_plot, detect_events, packets_to_table


class ProcessingTests(unittest.TestCase):
    def test_conversion(self):
        packets = generate_packets(2)
        table = packets_to_table(packets)
        self.assertEqual(table.shape, (2, 6))
        self.assertEqual(table.loc[1, 'Value_5'], 1.5)
        self.assertIn('DataPacketValue', packets[0])

    def test_empty(self):
        self.assertEqual(packets_to_table([]).shape, (0, 6))
        self.assertEqual(json.loads(build_plot([])), {})

    def test_missing_and_malformed(self):
        for packet in [{}, {'Timestamp': 0}, {'Timestamp': [], 'DataPacketValue': [0]*6},
                       {'Timestamp': 0, 'DataPacketValue': [0]*5},
                       {'Timestamp': 0, 'DataPacketValue': [None]*6},
                       {'Timestamp': 0, 'DataPacketValue': ['1']*6},
                       {'Timestamp': 0, 'DataPacketValue': [True]*6},
                       {'Timestamp': 0, 'DataPacketValue': [float('nan')]*6},
                       {'Timestamp': 0, 'DataPacketValue': [float('inf')]*6}]:
            with self.subTest(packet_type=str(type(packet))):
                with self.assertRaises(ValueError):
                    packets_to_table([packet])
        with self.assertRaises(ValueError):
            packets_to_table(2)

    def test_duplicate_timestamp(self):
        packets = generate_packets(2)
        packets[1]['Timestamp'] = 0
        self.assertEqual(packets_to_table(packets).loc[0, 'Value_0'], 1)

    def test_rank_selection(self):
        events = json.loads(build_plot(generate_packets()))
        self.assertEqual([r['index'] for r in events.values()], list(range(5, 15)))
        self.assertAlmostEqual(events['0']['Value'], 5.22)

    def test_short_input(self):
        self.assertEqual(json.loads(build_plot(generate_packets(5))), {})
        self.assertEqual(len(json.loads(build_plot(generate_packets(6)))), 1)

    def test_channel_four_is_excluded(self):
        packets = generate_packets()
        expected = build_plot(packets)
        for packet in packets:
            packet['DataPacketValue'][4] = 999999
        self.assertEqual(build_plot(packets), expected)

    def test_ties_preserve_all_matches(self):
        packets = [{'Timestamp': i, 'DataPacketValue': [1]*6} for i in range(20)]
        self.assertEqual(len(json.loads(build_plot(packets))), 20)

    def test_missing_table_channel(self):
        with self.assertRaises(ValueError):
            detect_events(packets_to_table([]).drop(columns=['Value_0']))


if __name__ == '__main__':
    unittest.main()
