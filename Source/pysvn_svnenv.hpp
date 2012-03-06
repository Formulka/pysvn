//
// ====================================================================
// (c) 2003-2009 Barry A Scott.  All rights reserved.
//
// This software is licensed as described in the file LICENSE.txt,
// which you should have received as part of this distribution.
//
// ====================================================================
//
#ifndef __PYSVN_SVNENV__
#define __PYSVN_SVNENV__

#include "CXX/Objects.hxx"

#ifndef PYCXX_MAKEVERSION
#error PyCXX version 5.3.5 is required
#endif

#if PYCXX_VERSION < PYCXX_MAKEVERSION( 5, 3, 5 )
#error PyCXX version 5.3.5 is required
#endif

#include <svn_version.h>
#include <svn_client.h>
#include <svn_dirent_uri.h>
#include <svn_fs.h>
#include <svn_repos.h>
#include <apr_xlate.h>
#include <string>

#if !defined( SVN_VER_MAJOR )
#error "SVN_VER_MAJOR not defined"
#endif

#if !defined( SVN_VER_MINOR )
#error "SVN_VER_MINOR not defined"
#endif

// SVN 1.1 or later
#if (SVN_VER_MAJOR == 1 && SVN_VER_MINOR >= 1) || SVN_VER_MAJOR > 1
#define PYSVN_HAS_CLIENT_ADD2
#define PYSVN_HAS_CLIENT_DIFF_PEG
#define PYSVN_HAS_CLIENT_EXPORT2
#define PYSVN_HAS_CLIENT_MERGE_PEG
#define PYSVN_HAS_CLIENT_VERSION
#endif

// SVN 1.2 or later
#if (SVN_VER_MAJOR == 1 && SVN_VER_MINOR >= 2) || SVN_VER_MAJOR > 1
#define PYSVN_HAS_CLIENT_ANNOTATE2
#define PYSVN_HAS_CLIENT_CAT2
#define PYSVN_HAS_CLIENT_CHECKOUT2
#define PYSVN_HAS_CLIENT_COMMIT2
#define PYSVN_HAS_CLIENT_DIFF_PEG2
#define PYSVN_HAS_CLIENT_DIFF2
#define PYSVN_HAS_CLIENT_EXPORT3
#define PYSVN_HAS_CLIENT_INFO
#define PYSVN_HAS_CLIENT_LOCK
#define PYSVN_HAS_CLIENT_LOG2
#define PYSVN_HAS_CLIENT_LS2
#define PYSVN_HAS_CLIENT_MOVE2
#define PYSVN_HAS_CLIENT_PROPGET2
#define PYSVN_HAS_CLIENT_PROPLIST2
#define PYSVN_HAS_CLIENT_PROPSET2
#define PYSVN_HAS_CLIENT_STATUS2
#define PYSVN_HAS_CLIENT_UPDATE2
#define PYSVN_HAS_CONTEXT_NOTIFY2
#define PYSVN_HAS_WC_ADM_PROBE_OPEN3
#endif

// SVN 1.3 or later
#if (SVN_VER_MAJOR == 1 && SVN_VER_MINOR >= 3) || SVN_VER_MAJOR > 1
#define PYSVN_HAS_SVN_CLIENT_COMMIT_ITEM2_T
#define PYSVN_HAS_SVN_COMMIT_INFO_T
#define PYSVN_HAS_CONTEXT_LOG_MSG2
#define PYSVN_HAS_CONTEXT_PROGRESS

#define PYSVN_HAS_WC_ADM_DIR

#define PYSVN_HAS_CLIENT_ADD3
#define PYSVN_HAS_CLIENT_COMMIT3
#define PYSVN_HAS_CLIENT_COPY2
#define PYSVN_HAS_CLIENT_DELETE2
#define PYSVN_HAS_CLIENT_DIFF_PEG3
#define PYSVN_HAS_CLIENT_DIFF3
#define PYSVN_HAS_CLIENT_IMPORT2
#define PYSVN_HAS_CLIENT_LS3
#define PYSVN_HAS_CLIENT_MKDIR2
#define PYSVN_HAS_CLIENT_MOVE3
#endif

// SVN 1.4 or later
#if (SVN_VER_MAJOR == 1 && SVN_VER_MINOR >= 4) || SVN_VER_MAJOR > 1
#define PYSVN_HAS_CLIENT_ANNOTATE3
#define PYSVN_HAS_CLIENT_COPY3
#define PYSVN_HAS_CLIENT_DIFF_SUMMARIZE
#define PYSVN_HAS_CLIENT_LIST
#define PYSVN_HAS_CLIENT_LOG3
#define PYSVN_HAS_CLIENT_MERGE2
#define PYSVN_HAS_CLIENT_MERGE_PEG2
#define PYSVN_HAS_CLIENT_MOVE4
#define PYSVN_HAS_DIFF_FILE_IGNORE_SPACE
#define PYSVN_HAS_SVN_AUTH_PROVIDERS
#define PYSVN_HAS_IO_OPEN_UNIQUE_FILE2
#endif

// SVN 1.5 or later
#if (SVN_VER_MAJOR == 1 && SVN_VER_MINOR >= 5) || SVN_VER_MAJOR > 1
#define PYSVN_HAS_SVN__DEPTH_PARAMETER
#define PYSVN_HAS_CLIENT_ADD4
#define PYSVN_HAS_CLIENT_ADD_TO_CHANGELIST
#define PYSVN_HAS_SVN_CLIENT_BLAME_RECEIVER2_T QQQ
#define PYSVN_HAS_CLIENT_ANNOTATE4
#define PYSVN_HAS_CLIENT_CHECKOUT3
#define PYSVN_HAS_CLIENT_COMMIT4
#define PYSVN_HAS_CLIENT_COPY4
#define PYSVN_HAS_SVN_CLIENT_CTX_T__CONFLICT_FUNC
#define PYSVN_HAS_SVN_CLIENT_CTX_T__LOG_MSG_FUNC3 QQQ
#define PYSVN_HAS_SVN_CLIENT_CTX_T__MIMETYPES_MAP QQQ
#define PYSVN_HAS_CLIENT_DELETE3
#define PYSVN_HAS_CLIENT_DIFF4
#define PYSVN_HAS_CLIENT_DIFF_PEG4
#define PYSVN_HAS_CLIENT_DIFF_SUMMARIZE2
#define PYSVN_HAS_CLIENT_DIFF_SUMMARIZE_PEG2
#define PYSVN_HAS_CLIENT_EXPORT4
#define PYSVN_HAS_CLIENT_GET_CHANGELIST
#define PYSVN_HAS_CLIENT_GET_CHANGELIST_STREAMY QQQ
#define PYSVN_HAS_SVN_CLIENT_GET_COMMIT_LOG3_T QQQ
#define PYSVN_HAS_CLIENT_IMPORT3
#define PYSVN_HAS_CLIENT_INFO2
#define PYSVN_HAS_CLIENT_LIST2
#define PYSVN_HAS_CLIENT_LOG4
#define PYSVN_HAS_CLIENT_MERGE3
#define PYSVN_HAS_CLIENT_MERGE_REINTEGRATE
#define PYSVN_HAS_CLIENT_MERGEINFO_GET_AVAILABLE QQQ
#define PYSVN_HAS_CLIENT_MERGEINFO_GET_MERGED QQQ
#define PYSVN_HAS_CLIENT_MERGE_PEG3 QQQ
#define PYSVN_HAS_CLIENT_MKDIR3
#define PYSVN_HAS_CLIENT_MOVE5
#define PYSVN_HAS_CLIENT_PROPGET3
#define PYSVN_HAS_CLIENT_PROPLIST3
#define PYSVN_HAS_CLIENT_PROPSET3
#define PYSVN_HAS_CLIENT_REMOVE_FROM_CHANGELISTS
#define PYSVN_HAS_CLIENT_RESOLVE
#define PYSVN_HAS_CLIENT_REVERT2
#define PYSVN_HAS_CLIENT_ROOT_URL_FROM_PATH
#define PYSVN_HAS_CLIENT_STATUS3
#define PYSVN_HAS_CLIENT_SUGGEST_MERGE_SOURCES QQQ
#define PYSVN_HAS_CLIENT_SWITCH2
#define PYSVN_HAS_CLIENT_UPDATE3
#define PYSVN_HAS_SVN_INFO_T__CHANGELIST
#define PYSVN_HAS_SVN_INFO_T__SIZES
#define PYSVN_HAS_SVN_WC_NOTIFY_ACTION_T__1_5 QQQ
#define PYSVN_HAS_SVN_WC_CONFLICT_CHOICE_T
#endif

// SVn 1.6 or later
#if (SVN_VER_MAJOR == 1 && SVN_VER_MINOR >= 6) || SVN_VER_MAJOR > 1
#define PYSVN_HAS_SVN_1_6
#define PYSVN_HAS_CLIENT_COPY5
#define PYSVN_HAS_IO_OPEN_UNIQUE_FILE3
#define PYSVN_HAS_CLIENT_LOG5
#define PYSVN_HAS_CLIENT_STATUS4
#define PYSVN_HAS_AUTH_GET_SIMPLE_PROVIDER2
#define PYSVN_HAS_AUTH_GET_SSL_CLIENT_CERT_PW_FILE_PROVIDER2
#define PYSVN_HAS_SVN_CLIENT_CTX_T__CONFLICT_FUNC_16
#define PYSVN_HAS_SVN_WC_OPERATION_T
#define PYSVN_HAS_SVN_WC_CONFLICT_RESULT_T__SAVE_MERGED

#endif

// SVN 1.7 or later
#if (SVN_VER_MAJOR == 1 && SVN_VER_MINOR >= 7) || SVN_VER_MAJOR > 1
#define PYSVN_HAS_SVN_1_7
#define PYSVN_HAS_CLIENT_BLAME5 QQQ
#define PYSVN_HAS_CLIENT_COMMIT5 QQQ
#define PYSVN_HAS_CLIENT_COPY6 QQQ
#define PYSVN_HAS_CLIENT_DELETE4 QQQ
#define PYSVN_HAS_CLIENT_DIFF5 QQQ
#define PYSVN_HAS_CLIENT_DIFF_PEG5 QQQ
#define PYSVN_HAS_CLIENT_EXPORT5 QQQ
#define PYSVN_HAS_CLIENT_GET_WC_ROOT QQQ
#define PYSVN_HAS_CLIENT_IMPORT4 QQQ
#define PYSVN_HAS_CLIENT_INFO2_T QQQ
#define PYSVN_HAS_CLIENT_INFO3 QQQ
#define PYSVN_HAS_CLIENT_INFO_RECEIVER2_T QQQ
#define PYSVN_HAS_CLIENT_MERGE4 QQQ
#define PYSVN_HAS_CLIENT_MERGEINFO_LOG QQQ
#define PYSVN_HAS_CLIENT_MERGE_PEG4 QQQ
#define PYSVN_HAS_CLIENT_MIN_MAX_REVISIONS QQQ
#define PYSVN_HAS_CLIENT_MKDIR4 QQQ
#define PYSVN_HAS_CLIENT_MOVE6 QQQ
#define PYSVN_HAS_CLIENT_PATCH QQQ
#define PYSVN_HAS_CLIENT_PATCH_FUNC_T QQQ
#define PYSVN_HAS_CLIENT_PROPGET4 QQQ
#define PYSVN_HAS_CLIENT_PROPSET_LOCAL QQQ
#define PYSVN_HAS_CLIENT_PROPSET_REMOTE QQQ
#define PYSVN_HAS_CLIENT_RELOCATE2 QQQ
#define PYSVN_HAS_CLIENT_STATUS5 QQQ
#define PYSVN_HAS_CLIENT_SWITCH3 QQQ
#define PYSVN_HAS_CLIENT_UPDATE4 QQQ
#define PYSVN_HAS_CLIENT_UPGRADE QQQ
#define PYSVN_HAS_CLIENT_URL_FROM_PATH2 QQQ
#define PYSVN_HAS_CLIENT_UUID_FROM_PATH2 QQQ
#endif


#if defined( PYSVN_HAS_CLIENT_STATUS3 )
typedef svn_wc_status2_t pysvn_wc_status_t;
#elif defined( PYSVN_HAS_CLIENT_STATUS2 )
typedef svn_wc_status2_t pysvn_wc_status_t;
#else
typedef svn_wc_status_t pysvn_wc_status_t;
#endif

#if defined( PYSVN_HAS_SVN_COMMIT_INFO_T )
typedef svn_commit_info_t pysvn_commit_info_t;
#else
typedef svn_client_commit_info_t pysvn_commit_info_t;
#endif

class SvnPool;
class SvnContext;
class SvnTransaction;

class SvnException
{
public:
    SvnException( svn_error_t *error );
    SvnException( const SvnException &other );

    virtual ~SvnException();

    // access methods
    Py::String &message();
    Py::Object &pythonExceptionArg( int style );
    apr_status_t code();

private:
    int                 m_code;
    Py::String          m_message;
    Py::Object          m_exception_arg;

private:
    SvnException();
    SvnException &operator=( const SvnException & );
};


class SvnPool
{
public:
    SvnPool( SvnContext &ctx );
    SvnPool( SvnTransaction &txn );
    ~SvnPool();

    operator apr_pool_t *() const;

private:
    apr_pool_t *m_pool;
};

class SvnContext
{
public:
    SvnContext( const std::string &config_dir="" );
    virtual ~SvnContext();

    operator svn_client_ctx_t *();
    svn_client_ctx_t *ctx();

    // only use this pool for data that has a life time
    // that matches the life time of the context
    apr_pool_t          *getContextPool();

    //
    // this method will be called to retrieve
    // authentication information
    //
    // WORKAROUND FOR apr_xlate PROBLEM: 
    // STRINGS ALREADY HAVE TO BE UTF8!!!
    //
    // @retval true continue
    //
    void installGetLogin( bool install );
    virtual bool contextGetLogin
        (
        const std::string &realm,
        std::string &username, 
        std::string &password,
        bool &may_save
        ) = 0;

    // 
    // this method will be called to notify about
    // the progress of an ongoing action
    //
    void installNotify( bool install );
#if defined( PYSVN_HAS_CONTEXT_NOTIFY2 )
    virtual void contextNotify2
        (
        const svn_wc_notify_t *notify,
        apr_pool_t *pool
        ) = 0;
#else
    virtual void contextNotify
        (
        const char *path,
        svn_wc_notify_action_t action,
        svn_node_kind_t kind,
        const char *mime_type,
        svn_wc_notify_state_t content_state,
        svn_wc_notify_state_t prop_state,
        svn_revnum_t revision
        ) = 0;
#endif


#if defined( PYSVN_HAS_CONTEXT_PROGRESS )
    void installProgress( bool install );
    virtual void contextProgress
        (
        apr_off_t progress,
        apr_off_t total
        ) = 0;
#endif

#if defined( PYSVN_HAS_SVN_CLIENT_CTX_T__CONFLICT_FUNC )
    void installConflictResolver( bool install );
    virtual bool contextConflictResolver
        (
        svn_wc_conflict_result_t **result,
        const svn_wc_conflict_description_t *description,
        apr_pool_t *pool
        ) = 0;
#endif

    //
    // this method will be called periodically to allow
    // the app to cancel long running operations
    //
    // @return cancel action?
    // @retval true cancel
    //
    void installCancel( bool install );
    virtual bool contextCancel
        (
        ) = 0;

    //
    // this method will be called to retrieve
    // a log message
    //
    virtual bool contextGetLogMessage
        (
        std::string &msg
        ) = 0;

    //
    // this method is called if there is ssl server
    // information, that has to be confirmed by the user
    //
    // @param data 
    // @return @a SslServerTrustAnswer
    //
    virtual bool contextSslServerTrustPrompt
        (
        const svn_auth_ssl_server_cert_info_t &info, 
        const std::string &relam,
        apr_uint32_t &acceptedFailures,
        bool &accept_permanent
        ) = 0;

    //
    // this method is called to retrieve client side
    // information
    //
    virtual bool contextSslClientCertPrompt
        (
        std::string &cert_file, const std::string &realm, bool &may_save
        ) = 0;

    //
    // this method is called to retrieve the password
    // for the certificate
    //
    // @param password
    //
    virtual bool contextSslClientCertPwPrompt
        (
        std::string &password,
        const std::string &realm,
        bool &may_save
        ) = 0;

private:
    apr_pool_t          *m_pool;
    svn_client_ctx_t    *m_context;
    char                *m_config_dir;
};

class SvnTransaction
{
public:
    SvnTransaction();
    ~SvnTransaction();

    svn_error_t *init( const std::string &repos_path, const std::string &transaction,
        bool is_revision );

    operator svn_fs_txn_t *();
    svn_fs_txn_t *transaction();
    operator svn_fs_t *();
    operator svn_repos_t *();
    svn_revnum_t revision();
    bool is_revision() const { return m_txn == NULL; };
    svn_error_t *root( svn_fs_root_t **root, apr_pool_t *pool );

private:
    apr_pool_t          *m_pool;
    svn_repos_t         *m_repos;
    svn_fs_t            *m_fs;
    svn_fs_txn_t        *m_txn;
    char                *m_txn_name;
    svn_revnum_t         m_rev_id;
};

#endif // __PYSVN_SVNENV__
