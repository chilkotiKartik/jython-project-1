# -*- coding: utf-8 -*-
from javax.sound.midi import MidiSystem, ShortMessage, Sequence, MidiEvent
from java.util import Random
import java.io.File as JFile



# === Settings ===
TEMPO_BPM = 80
TICKS_PER_BEAT = 480
DURATION_SECONDS = 35
TOTAL_BEATS = (TEMPO_BPM * DURATION_SECONDS) // 60

INSTRUMENT_CHORDS = 4   # Electric Piano
INSTRUMENT_MELODY = 73  # Flute
CHANNEL_CHORDS = 0
CHANNEL_MELODY = 1

CHORDS = [
    [60, 64, 67],
    [62, 65, 69],
    [59, 63, 67],
    [57, 60, 64],
]

MELODY_NOTES = [72, 74, 76, 77, 79, 81, 83]

def create_note(channel, pitch, velocity, start_tick, duration):
    on = ShortMessage()
    on.setMessage(ShortMessage.NOTE_ON, channel, pitch, velocity)
    off = ShortMessage()
    off.setMessage(ShortMessage.NOTE_OFF, channel, pitch, 0)
    return [
        MidiEvent(on, start_tick),
        MidiEvent(off, start_tick + duration)
    ]

sequence = Sequence(Sequence.PPQ, TICKS_PER_BEAT)
track = sequence.createTrack()

def set_instrument(channel, instrument, tick):
    msg = ShortMessage()
    msg.setMessage(ShortMessage.PROGRAM_CHANGE, channel, instrument, 0)
    track.add(MidiEvent(msg, tick))

set_instrument(CHANNEL_CHORDS, INSTRUMENT_CHORDS, 0)
set_instrument(CHANNEL_MELODY, INSTRUMENT_MELODY, 0)

tick = 0
for i in range(0, TOTAL_BEATS, 2):
    chord = CHORDS[i % len(CHORDS)]
    for note in chord:
        for ev in create_note(CHANNEL_CHORDS, note, 80, tick, TICKS_PER_BEAT * 2):
            track.add(ev)
    tick += TICKS_PER_BEAT * 2

random = Random()
for i in range(40):
    note = MELODY_NOTES[random.nextInt(len(MELODY_NOTES))]
    start_tick = TICKS_PER_BEAT * random.nextInt(TOTAL_BEATS)
    duration = TICKS_PER_BEAT // 2
    for ev in create_note(CHANNEL_MELODY, note, 100, start_tick, duration):
        track.add(ev)

output_file = JFile("output_melody.mid")
MidiSystem.write(sequence, 1, output_file)
print("Saved to: output_melody.mid")

sequencer = MidiSystem.getSequencer()
sequencer.open()
sequencer.setSequence(sequence)
sequencer.setTempoInBPM(TEMPO_BPM)
sequencer.start()

while sequencer.isRunning():
    pass

sequencer.stop()
sequencer.close()
print(" Melody playback complete.")
