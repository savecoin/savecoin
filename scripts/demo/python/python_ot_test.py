#!/usr/bin/env python
#
# This script demonstrates both the high-level AND low-level
# OT API, in the Python language.
#
# Before running this script, make sure the _otapi.so and
# the otapi.py are both in a folder on the path:  $PYTHONPATH
# Personally I put them in /usr/local/lib/python2.7/site-packages
# and then I set $PYTHONPATH to contain that path.
#
# Also, make sure the server is running ('otserver')
#
nb = raw_input('\n\
    nBefore running this script, make sure the _otapi.so and\nthe otapi.py are both in a folder on the path:  $PYTHONPATH\nPersonally I put them in /usr/local/lib/python2.7/site-packages\nand then I set $PYTHONPATH to contain that path.\n\nAlso, make sure the server is running (otserver)\n\nOkay, ready to test?\nPress enter TWICE to try out the OT API... ')

# ---------------------------------------------------------
import otapi

# These functions are perfect examples of the 'Low-level API',
# which is useful for simple functions that don't require messaging
# any OT servers. See OTAPI.hpp for the complete low-level API.

otapi.OTAPI_Wrap_AppInit()
otapi.OTAPI_Wrap_LoadWallet()

# ---------------------------------------------------------
# Use the low-level API to see how many server contracts
# are in the user's wallet.

count = otapi.OTAPI_Wrap_GetServerCount()
print 'Server count: ', count

# ---------------------------------------------------------

# OT MADE EASY  (high-level API)
#
# This object handles all the request/response going on with
# any servers, plus all the retries and synchronization. It's
# the 'High-level API'. See OT_ME.h for the complete set of
# high-level API functions.

objEasy = otapi.OT_ME()

# ---------------------------------------------------------
#
# Use the High-level API to download a user's public key from
# the server. (Obviously this will fail if the server is not
# running, or if the test data is not installed.)
strCheck = objEasy.check_user('r1fUoHwJOWCuK3WBAAySjmKYqsG6G2TYIxdqY6YNuuG', 'DYEB6U7dcpbwdGrftPnslNKz76BDuBTFAjiAgKaiY2n', 'HpDoVBTix9GRLvZZoKBi2zv2f4IFVLmRrW2Q0nAA0OH')

# ---------------------------------------------------------
# objEasy.check_user corresponds to the command-line:
#   'opentxs checknym'
#
# It's a useful test because it shows whether a server message
# is successful, before going the extra step of trying a real
# financial transaction.
#
# Therefore we only need to verify the Message Success, and not
# any transaction success. (Remember, a successful message can
# still contain a failed transaction.)

nResult = objEasy.VerifyMessageSuccess(strCheck)

if nResult < 0:
    print 'Error in check nym. Is the server running? Is the test data in ~/.ot ?'
elif nResult == 0:
    print 'Failure in check nym. Is the test data in ~/.ot ?'
elif nResult == 1:
    print 'Success in check nym.'
else:
    print 'Unexpected return value in check nym.'

# ---------------------------------------------------------
#
# Use the high-level API to withdraw some cash (1 silver gram)
# from FT's Silver account. (Obviously this will not work if the
# localhost server is not running, or if the test data is not
# installed to ~/.ot )

# Make sure we have the proper mint...
objEasy.load_or_retrieve_mint("r1fUoHwJOWCuK3WBAAySjmKYqsG6G2TYIxdqY6YNuuG", \
    "DYEB6U7dcpbwdGrftPnslNKz76BDuBTFAjiAgKaiY2n", \
    "7f8nlUn795x8931JParRnmKAyw8cegRyBMcFg9FccaF")

if objEasy.VerifyMessageSuccess(strCheck) < 0:
  print 'Failure: Unable to load or retrieve necessary mint file for withdrawal...'


# This is a "real" financial transaction:
#
strWithdraw = objEasy.withdraw_cash('r1fUoHwJOWCuK3WBAAySjmKYqsG6G2TYIxdqY6YNuuG', 'DYEB6U7dcpbwdGrftPnslNKz76BDuBTFAjiAgKaiY2n', 'yQGh0vgm9YiqYOh6bfLDxyAA7Nnh2NmturCQmOt4LTo', '1')

# ---------------------------------------------------------
# InterpretTransactionMsgReply
#
# This function first verifies whether the message itself was a success.
# (For example, what if the server was down, and never received it?)
#
# Once it verifies that the reply was successful as a message, then it
# peers deeper, to see whether the balance agreement was successful as well.
# (After all, any transaction is automatically rejected if the balance
# agreement is poorly-formed.)
#
# Then if the balance agreement was successful, then finally, this same
# function (InterpretTransactionMsgReply) checks to see whether the
# transaction ITSELF was successful. After all, maybe there was an error
# saving it back to disk on the server side and this caused the transaction
# to fail. Or maybe there wasn't enough money in the account. Etc. All of
# the above work is done in the below call:

nResult = objEasy.InterpretTransactionMsgReply('r1fUoHwJOWCuK3WBAAySjmKYqsG6G2TYIxdqY6YNuuG', 'DYEB6U7dcpbwdGrftPnslNKz76BDuBTFAjiAgKaiY2n', 'yQGh0vgm9YiqYOh6bfLDxyAA7Nnh2NmturCQmOt4LTo', 'withdraw_cash', strWithdraw)

if nResult < 0:
    print '\nError in withdraw cash. Is the server running? Is the test data in ~/.ot ?'
elif nResult == 0:
    print '\nFailure in withdraw cash. Is the test data installed in ~/.ot ?'
elif nResult == 1:
    print '\nSuccess in withdraw cash! (Using high-level API in Python.)'
else:
    print '\nUnexpected return value in withdraw cash.'

# ---------------------------------------------------------

# At this point we're done. We've downloaded a public key from
# the OT server, and we've also withdrawn a little cash from the
# server. We've demonstrated that both the high-level and low-level
# OT APIs are operational through Python.

# So... we're done. Let's shutdown OT and finish execution.
# (Using the low-level API...)

otapi.OTAPI_Wrap_Output(0, "\nOne more thing: Successfully used OT_API_Output.\n")

otapi.OTAPI_Wrap_AppCleanup()


# P.S. to see the complete OT high-level API:  OT_ME.hpp
#  and to see the complete OT low-level  API:  OTAPI.hpp
#
# See the Open-Transactions/include/otapi folder for all
# relevant headers.
#
# One more thing: If you want to see a lot of free sample code
# similar to the above code, which shows you how to use all the
# different OT API function calls, check out this file:
#
#        Open-Transactions/scripts/ot/ot_commands.ot
#
# (It contains the complete implementation for a command-line
#  Open-Transactions client.)
# --------------------------------------
