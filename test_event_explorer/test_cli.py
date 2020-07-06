import os

from click.testing import CliRunner
import pandas as pd

import event_explorer.cli as cli


MOCK_EVENTS = pd.DataFrame(
    {"id": ["abcd", "efgh"], "name": ["big event", "little event"]}
)


MOCK_ATTENDEES = {
    "big event": pd.DataFrame(
        {"first name": ["Matt", "Nathan"], "last name": ["Robinson", "Smuckler"]}
    ),
    "little event": pd.DataFrame(
        {"first name": ["Matt", "Nathan"], "last name": ["Robinson", "Smuckler"]}
    ),
}


def test_events_to_csv(monkeypatch, tmpdir):
    def mock_load_fake_source(*args, **kwargs):
        return MOCK_EVENTS, MOCK_ATTENDEES

    monkeypatch.setattr(cli, "LOAD_OPTIONS", {"fake_source": mock_load_fake_source})
    runner = CliRunner()
    result = runner.invoke(
        cli.main,
        ["events-to-csv", "--directory", tmpdir.dirname, "--source", "fake_source"],
    )

    events = pd.read_csv(os.path.join(tmpdir.dirname, "fake_source.csv"))
    pd.testing.assert_frame_equal(events, MOCK_EVENTS)

    big_event = pd.read_csv(
        os.path.join(tmpdir.dirname, "fake_source", "big-event.csv")
    )
    pd.testing.assert_frame_equal(big_event, MOCK_ATTENDEES["big event"])

    little_event = pd.read_csv(
        os.path.join(tmpdir.dirname, "fake_source", "little-event.csv")
    )
    pd.testing.assert_frame_equal(little_event, MOCK_ATTENDEES["big event"])
