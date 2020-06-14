// Copyright (c) 2009-2010 Satoshi Nakamoto
// Copyright (c) 2009-2016 The Bitcoin Core developers
// Copyright (c) 2019 Bitcoin Association
// Copyright (c) 2020* Jimmy N. Lose
// * Gregorian calendar years
// Distributed under the Open BSV software license, see the accompanying file LICENSE.

#ifndef BITCOIN_INIT_H
#define BITCOIN_INIT_H

#include <string>
#include "taskcancellation.h"

class Config;
class CScheduler;
class CWallet;

namespace boost {
class thread_group;
} // namespace boost

void StartShutdown();
task::CCancellationToken GetShutdownToken();
/** Interrupt threads */
void Interrupt(boost::thread_group &threadGroup);
void Shutdown();
//! Initialize the logging infrastructure
void InitLogging();
//! Parameter interaction: change current parameters depending on various rules
void InitParameterInteraction();

/** Initialize bitcoin core: Basic context setup.
 *  @note This can be done before daemonization.
 *  @pre Parameters should be parsed and config file should be read.
 */
bool AppInitBasicSetup();
/**
 * Initialization: parameter interaction.
 * @note This can be done before daemonization.
 * @pre Parameters should be parsed and config file should be read,
 * AppInitBasicSetup should have been called.
 */
bool AppInitParameterInteraction(Config &config);
/**
 * Initialization sanity checks: ecc init, sanity checks, dir lock.
 * @note This can be done before daemonization.
 * @pre Parameters should be parsed and config file should be read,
 * AppInitParameterInteraction should have been called.
 */
bool AppInitSanityChecks();
/**
 * Bitcoin core main initialization.
 * @note This should only be done after daemonization.
 * @pre Parameters should be parsed and config file should be read,
 * AppInitSanityChecks should have been called.
 */
bool AppInitMain(Config &config, boost::thread_group &threadGroup,
                 CScheduler &scheduler, const task::CCancellationToken& shutdownToken);

/** The help message mode determines what help message to show */
enum HelpMessageMode { HMM_BITCOIND };

/** Help for options shared between UI and daemon (for -help) */
std::string HelpMessage(HelpMessageMode mode);
/** Returns licensing information (for -version) */
std::string LicenseInfo();

#endif // BITCOIN_INIT_H
