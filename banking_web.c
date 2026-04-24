/*
 * ============================================================
 *  BANKING SYSTEM - Web Version (command-line interface)
 *  Designed to be called by Flask server as a subprocess.
 *
 *  Usage examples:
 *    banking_web.exe create "John Doe" 50000 1234
 *    banking_web.exe deposit 1001 20000
 *    banking_web.exe withdraw 1001 5000 1234
 *    banking_web.exe balance 1001 1234
 *    banking_web.exe transfer 1001 1002 10000 1234
 *    banking_web.exe delete 1001 1234
 *    banking_web.exe admin_login <password>
 *    banking_web.exe history
 *    banking_web.exe list
 *
 *  All output is JSON so Flask can parse it easily.
 * ============================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ACCOUNTS  100
#define ACCOUNTS_FILE "accounts.dat"
#define LOG_FILE      "transactions.log"
#define NAME_LEN       50
#define ADMIN_PASSWORD "admin123"

typedef struct {
    int   accountNumber;
    char  holderName[NAME_LEN];
    float balance;
    int   pin;
} Account;

Account accounts[MAX_ACCOUNTS];
int     totalAccounts = 0;
int     nextAccountNum = 1001;

/* ── File helpers ─────────────────────────────────────── */

void loadAccounts() {
    FILE *fp = fopen(ACCOUNTS_FILE, "rb");
    if (!fp) return;
    fread(&totalAccounts,  sizeof(int),     1,             fp);
    fread(&nextAccountNum, sizeof(int),     1,             fp);
    fread(accounts,        sizeof(Account), totalAccounts, fp);
    fclose(fp);
}

void saveAccounts() {
    FILE *fp = fopen(ACCOUNTS_FILE, "wb");
    if (!fp) return;
    fwrite(&totalAccounts,  sizeof(int),     1,             fp);
    fwrite(&nextAccountNum, sizeof(int),     1,             fp);
    fwrite(accounts,        sizeof(Account), totalAccounts, fp);
    fclose(fp);
}

void logTransaction(int accNum, const char *type, float amount) {
    FILE *fp = fopen(LOG_FILE, "a");
    if (!fp) return;
    fprintf(fp, "{\"account\":%d,\"type\":\"%s\",\"amount\":%.2f}\n",
            accNum, type, amount);
    fclose(fp);
}

int findAccount(int accNum) {
    for (int i = 0; i < totalAccounts; i++)
        if (accounts[i].accountNumber == accNum) return i;
    return -1;
}

/* ── JSON output helpers ─────────────────────────────── */

void jsonOk(const char *msg) {
    printf("{\"status\":\"ok\",\"message\":\"%s\"}\n", msg);
}

void jsonError(const char *msg) {
    printf("{\"status\":\"error\",\"message\":\"%s\"}\n", msg);
}

/* ── Commands ────────────────────────────────────────── */

/*
 * create <name> <initial_deposit> <pin>
 * Creates a new account and prints the account number as JSON.
 */
void cmdCreate(int argc, char *argv[]) {
    if (argc < 5) { jsonError("Usage: create <name> <deposit> <pin>"); return; }
    if (totalAccounts >= MAX_ACCOUNTS) { jsonError("Bank system is full - cannot create new accounts"); return; }

    Account a;
    a.accountNumber = nextAccountNum++;
    strncpy(a.holderName, argv[2], NAME_LEN - 1);
    a.balance = atof(argv[3]);
    a.pin     = atoi(argv[4]);

    if (a.balance < 0) { jsonError("Initial deposit cannot be negative"); return; }
    if (strlen(argv[2]) == 0) { jsonError("Name cannot be empty"); return; }

    accounts[totalAccounts++] = a;
    saveAccounts();
    logTransaction(a.accountNumber, "CREATED", a.balance);

    printf("{\"status\":\"ok\",\"accountNumber\":%d,\"name\":\"%s\",\"balance\":%.2f}\n",
           a.accountNumber, a.holderName, a.balance);
}

/*
 * deposit <accountNumber> <amount>
 */
void cmdDeposit(int argc, char *argv[]) {
    if (argc < 4) { jsonError("Usage: deposit <accNum> <amount>"); return; }

    int   accNum = atoi(argv[2]);
    float amount = atof(argv[3]);
    int   idx    = findAccount(accNum);

    if (idx == -1)    { jsonError("Account not found - please verify account number"); return; }
    if (amount <= 0)  { jsonError("Deposit amount must be greater than zero"); return; }

    accounts[idx].balance += amount;
    saveAccounts();
    logTransaction(accNum, "DEPOSIT", amount);

    printf("{\"status\":\"ok\",\"accountHolder\":\"%s\",\"balance\":%.2f,\"message\":\"Successfully deposited UGX %.2f to account\"}\n",
           accounts[idx].holderName, accounts[idx].balance, amount);
}

/*
 * withdraw <accountNumber> <amount> <pin>
 */
void cmdWithdraw(int argc, char *argv[]) {
    if (argc < 5) { jsonError("Usage: withdraw <accNum> <amount> <pin>"); return; }

    int   accNum = atoi(argv[2]);
    float amount = atof(argv[3]);
    int   pin    = atoi(argv[4]);
    int   idx    = findAccount(accNum);

    if (idx == -1)                          { jsonError("Account not found - please verify account number"); return; }
    if (accounts[idx].pin != pin)           { jsonError("Incorrect PIN - withdrawal cancelled for security"); return; }
    if (amount <= 0)                        { jsonError("Withdrawal amount must be greater than zero"); return; }
    if (amount > accounts[idx].balance)     { jsonError("Insufficient funds - cannot withdraw more than balance"); return; }

    accounts[idx].balance -= amount;
    saveAccounts();
    logTransaction(accNum, "WITHDRAWAL", amount);

    printf("{\"status\":\"ok\",\"accountHolder\":\"%s\",\"balance\":%.2f,\"message\":\"Successfully withdrew UGX %.2f from account\"}\n",
           accounts[idx].holderName, accounts[idx].balance, amount);
}

/*
 * balance <accountNumber> <pin>
 */
void cmdBalance(int argc, char *argv[]) {
    if (argc < 4) { jsonError("Usage: balance <accNum> <pin>"); return; }

    int accNum = atoi(argv[2]);
    int pin    = atoi(argv[3]);
    int idx    = findAccount(accNum);

    if (idx == -1)                { jsonError("Account not found - please verify account number"); return; }
    if (accounts[idx].pin != pin) { jsonError("Incorrect PIN - access denied"); return; }

    printf("{\"status\":\"ok\",\"accountNumber\":%d,\"name\":\"%s\",\"balance\":%.2f}\n",
           accNum, accounts[idx].holderName, accounts[idx].balance);
}

/*
 * transfer <fromAcc> <toAcc> <amount> <pin>
 */
void cmdTransfer(int argc, char *argv[]) {
    if (argc < 6) { jsonError("Usage: transfer <from> <to> <amount> <pin>"); return; }

    int   fromNum = atoi(argv[2]);
    int   toNum   = atoi(argv[3]);
    float amount  = atof(argv[4]);
    int   pin     = atoi(argv[5]);

    int fromIdx = findAccount(fromNum);
    int toIdx   = findAccount(toNum);

    if (fromIdx == -1)                            { jsonError("Source account not found - please verify account number"); return; }
    if (toIdx   == -1)                            { jsonError("Destination account not found - please verify recipient account"); return; }
    if (accounts[fromIdx].pin != pin)             { jsonError("Incorrect PIN - transfer cancelled"); return; }
    if (fromNum == toNum)                         { jsonError("Cannot transfer to same account"); return; }
    if (amount <= 0)                              { jsonError("Transfer amount must be greater than zero"); return; }
    if (amount > accounts[fromIdx].balance)       { jsonError("Insufficient funds for this transfer"); return; }

    accounts[fromIdx].balance -= amount;
    accounts[toIdx].balance   += amount;
    saveAccounts();
    logTransaction(fromNum, "TRANSFER_OUT", amount);
    logTransaction(toNum,   "TRANSFER_IN",  amount);

    printf("{\"status\":\"ok\",\"newBalance\":%.2f,\"message\":\"Transfer of UGX %.2f successful to %s\",\"recipientName\":\"%s\"}\n",
           accounts[fromIdx].balance, amount, accounts[toIdx].holderName, accounts[toIdx].holderName);
}

/*
 * delete <accountNumber> <pin>
 * Deletes an account and removes it from the array.
 */
void cmdDelete(int argc, char *argv[]) {
    if (argc < 4) { jsonError("Usage: delete <accNum> <pin>"); return; }

    int accNum = atoi(argv[2]);
    int pin    = atoi(argv[3]);
    int idx    = findAccount(accNum);

    if (idx == -1)                    { jsonError("Account not found"); return; }
    if (accounts[idx].pin != pin)     { jsonError("Incorrect PIN - cannot delete account"); return; }

    char holderName[NAME_LEN];
    strncpy(holderName, accounts[idx].holderName, NAME_LEN - 1);
    float balance = accounts[idx].balance;

    /* Remove account by shifting array */
    for (int i = idx; i < totalAccounts - 1; i++)
        accounts[i] = accounts[i + 1];
    totalAccounts--;
    saveAccounts();
    logTransaction(accNum, "ACCOUNT_DELETED", balance);

    printf("{\"status\":\"ok\",\"message\":\"Account for %s (Acc #%d) has been deleted successfully\"}\n",
           holderName, accNum);
}

/*
 * admin_login <password>
 * Simple admin authentication.
 */
void cmdAdminLogin(int argc, char *argv[]) {
    if (argc < 3) { jsonError("Usage: admin_login <password>"); return; }

    const char *provided = argv[2];
    if (strcmp(provided, ADMIN_PASSWORD) == 0) {
        printf("{\"status\":\"ok\",\"message\":\"Admin login successful\",\"authenticated\":true}\n");
    } else {
        printf("{\"status\":\"error\",\"message\":\"Invalid admin password\",\"authenticated\":false}\n");
    }
}

/*
 * list  — returns all accounts as a JSON array (no PIN required, admin view)
 */
void cmdList() {
    printf("[");
    for (int i = 0; i < totalAccounts; i++) {
        if (i > 0) printf(",");
        printf("{\"accountNumber\":%d,\"name\":\"%s\",\"balance\":%.2f}",
               accounts[i].accountNumber,
               accounts[i].holderName,
               accounts[i].balance);
    }
    printf("]\n");
}

/*
 * history — prints the transaction log as a JSON array
 */
void cmdHistory() {
    FILE *fp = fopen(LOG_FILE, "r");
    if (!fp) { printf("[]\n"); return; }

    printf("[");
    char line[200];
    int first = 1;
    while (fgets(line, sizeof(line), fp)) {
        /* strip newline */
        line[strcspn(line, "\n")] = 0;
        if (!first) printf(",");
        printf("%s", line);
        first = 0;
    }
    printf("]\n");
    fclose(fp);
}

/* ── Main ────────────────────────────────────────────── */

int main(int argc, char *argv[]) {
    if (argc < 2) {
        jsonError("No command given");
        return 1;
    }

    loadAccounts();

    if      (strcmp(argv[1], "create")       == 0) cmdCreate(argc, argv);
    else if (strcmp(argv[1], "deposit")      == 0) cmdDeposit(argc, argv);
    else if (strcmp(argv[1], "withdraw")     == 0) cmdWithdraw(argc, argv);
    else if (strcmp(argv[1], "balance")      == 0) cmdBalance(argc, argv);
    else if (strcmp(argv[1], "transfer")     == 0) cmdTransfer(argc, argv);
    else if (strcmp(argv[1], "delete")       == 0) cmdDelete(argc, argv);
    else if (strcmp(argv[1], "admin_login")  == 0) cmdAdminLogin(argc, argv);
    else if (strcmp(argv[1], "list")         == 0) cmdList();
    else if (strcmp(argv[1], "history")      == 0) cmdHistory();
    else jsonError("Unknown command");

    return 0;
}
