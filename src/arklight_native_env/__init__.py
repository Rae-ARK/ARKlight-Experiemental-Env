"""arklight_native_env -- experimental, non-Web native rendering
environment for ARKlight's Website IR.

This package is Stage 0 scaffold only (see docs/ARCHITECTURE.md,
"Implementation staging"). It does not render anything yet. It only
proves that this repo can obtain and inspect arklight's IR as a
library consumer, without touching arklight's `android` packaging
subcommand, its WebView template, or its HTML backend output.

CURRENT_STAGE is a plain marker other modules/tests can check so it's
obvious, at a glance, which stage's guarantees currently hold.
"""

CURRENT_STAGE = 0
